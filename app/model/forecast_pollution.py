# app/model/forecast_pollution.py
import os
import requests
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from datetime import datetime, timezone

# 🌐 Configuration
API_KEY = "4532fc36b320a237f0dd40f12a2ffa04"
LAT, LON = 28.6139, 77.2090  # Delhi records

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FORECAST_WEATHER_CSV = os.path.join(BASE_DIR, "../data/output/forecast_weather.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "../data/output")
MODEL_DIR = BASE_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ❗ Load trained models
pm25_model = joblib.load(os.path.join(MODEL_DIR, "rf_regressor_pm25.pkl"))
pm10_model = joblib.load(os.path.join(MODEL_DIR, "rf_regressor_pm10.pkl"))

# 🌀 Fetch pollutant forecast (4 days, hourly) via OpenWeather Air Pollution API
pollut_url = (
    f"http://api.openweathermap.org/data/2.5/air_pollution/forecast"
    f"?lat={LAT}&lon={LON}&appid={API_KEY}"
)
#load pollute_records
res = requests.get(pollut_url)
res.raise_for_status()
pollut_data = res.json().get("list", [])

pollut_records = []
for entry in pollut_data:
    dt = datetime.fromtimestamp(entry["dt"], tz=timezone.utc)
    comp = entry["components"]
    comp["datetime"] = dt
    pollut_records.append(comp)
pollut_df = pd.DataFrame(pollut_records)

# ⛅ Load weather features from forecast_weather.csv
weather = pd.read_csv(FORECAST_WEATHER_CSV)
weather["datetime"] = pd.to_datetime(weather["datetime"])

# 🔄 Merge pollutant + weather forecasts
pollut_df["datetime"] = pd.to_datetime(pollut_df["datetime"], utc=True).dt.tz_localize(None)
weather["datetime"]   = pd.to_datetime(weather["datetime"], utc=False)

df = pd.merge_asof(
    pollut_df.sort_values("datetime"),
    weather.sort_values("datetime"),
    on="datetime",
    direction="nearest"
).dropna()


# Time features
df["hour"] = df["datetime"].dt.hour
df["dayofweek"] = df["datetime"].dt.dayofweek

# Required feature columns (& ensure numeric)
features = ["co","no2","o3","so2","nh3","temperature","humidity","wind_speed","hour","dayofweek"]
df = df[["datetime"] + features].dropna()

# Predictions
df["pred_pm25"] = pm25_model.predict(df[features])
df["pred_pm10"] = pm10_model.predict(df[features])

# Classification
def categorize_pm25(val):
    if val <= 30: return "Good"
    if val <= 60: return "Moderate"
    if val <= 90: return "Poor"
    if val <= 120: return "Unhealthy"
    if val <= 250: return "Severe"
    return "Hazardous"
def categorize_pm10(val):
    if val <= 50: return "Good"
    if val <= 100: return "Moderate"
    if val <= 250: return "Poor"
    if val <= 350: return "Unhealthy"
    if val <= 430: return "Severe"
    return "Hazardous"

df["cat_pm25"] = df["pred_pm25"].apply(categorize_pm25)
df["cat_pm10"] = df["pred_pm10"].apply(categorize_pm10)

# Save CSV output
out_cols = ["datetime","pred_pm25","cat_pm25","pred_pm10","cat_pm10"]
df[out_cols].to_csv(os.path.join(OUTPUT_DIR,"future_pollution_forecast.csv"), index=False)

# Plot next 48h forecast
subset = df.iloc[:48]
plt.figure(figsize=(12,6))
plt.plot(subset["datetime"], subset["pred_pm25"], 'o-', label="PM2.5 Forecast")
plt.plot(subset["datetime"], subset["pred_pm10"], 'x-', label="PM10 Forecast")
plt.xticks(rotation=25)
plt.xlabel("Datetime")
plt.ylabel("Pollutant Concentration (μg/m³)")

plt.title("48‑Hour PM2.5 & PM10 Forecast + Categories in CSV")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "pollution_48h_forecast.png"))
plt.close()

print("✅ Forecast + classifications saved (CSV + PNG)")
