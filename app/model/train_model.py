# train_model.py (Enhanced: PM2.5 & PM10 prediction with classification + weather features & 24-hour graph + full dataset training)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/output/historical_aqi_openweather.csv")
WEATHER_PATH = os.path.join(BASE_DIR, "../data/output/forecast_weather.csv")
MODEL_DIR = os.path.join(BASE_DIR, "../model")
PLOT_DIR = os.path.join(BASE_DIR, "../data/output")
PREDICTIONS_PATH_PM25 = os.path.join(PLOT_DIR, "pm25_predictions.csv")
PREDICTIONS_PATH_PM10 = os.path.join(PLOT_DIR, "pm10_predictions.csv")

os.makedirs(MODEL_DIR, exist_ok=True)

# Load AQI and weather data
df = pd.read_csv(DATA_PATH)
weather = pd.read_csv(WEATHER_PATH)
weather["datetime"] = pd.to_datetime(weather["datetime"])
df["datetime"] = pd.to_datetime(df["datetime"])

# Merge weather features
df = pd.merge_asof(df.sort_values("datetime"), weather.sort_values("datetime"), on="datetime", direction="nearest")
df.dropna(inplace=True)

# Time-based features
df["hour"] = df["datetime"].dt.hour
df["dayofweek"] = df["datetime"].dt.dayofweek

# Define input features
features = ["co", "no2", "o3", "so2", "nh3", "temperature", "humidity", "wind_speed", "hour", "dayofweek"]

##############################
# ===== PM2.5 Prediction =====
##############################
X_pm25 = df[features]
y_pm25 = df["pm2_5"]
X_train_p25, X_test_p25, y_train_p25, y_test_p25 = train_test_split(X_pm25, y_pm25, test_size=0.2, random_state=42)

model_pm25 = RandomForestRegressor(n_estimators=100, random_state=42)
model_pm25.fit(X_train_p25, y_train_p25)
y_pred_p25 = model_pm25.predict(X_test_p25)

r2_p25 = r2_score(y_test_p25, y_pred_p25)
mse_p25 = mean_squared_error(y_test_p25, y_pred_p25)
cv_scores_p25 = cross_val_score(model_pm25, X_pm25, y_pm25, scoring="r2", cv=KFold(n_splits=5, shuffle=True, random_state=42))

# Classification
def categorize_pm25(pm25):
    if pm25 <= 30:
        return "Good"
    elif pm25 <= 60:
        return "Moderate"
    elif pm25 <= 90:
        return "Poor"
    elif pm25 <= 120:
        return "Unhealthy"
    elif pm25 <= 250:
        return "Severe"
    else:
        return "Hazardous"

# Save PM2.5 model & results
joblib.dump(model_pm25, os.path.join(MODEL_DIR, "rf_regressor_pm25.pkl"))
df_pm25 = pd.DataFrame({"Actual_PM2.5": y_test_p25.values, "Predicted_PM2.5": y_pred_p25})
df_pm25["Category"] = df_pm25["Predicted_PM2.5"].apply(categorize_pm25)
df_pm25.to_csv(PREDICTIONS_PATH_PM25, index=False)

# Plot PM2.5 for last 24 hours
df_recent_pm25 = df.tail(24)
y_recent_pm25 = model_pm25.predict(df_recent_pm25[features])

plt.figure(figsize=(10, 5))
plt.plot(df_recent_pm25["datetime"], df_recent_pm25["pm2_5"], label="Actual PM2.5", marker="o")
plt.plot(df_recent_pm25["datetime"], y_recent_pm25, label="Predicted PM2.5", marker="x")
plt.title("PM2.5 Prediction (Last 24 Hours)")
plt.xlabel("Datetime")
plt.ylabel("PM2.5 Concentration")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "rf_pm25_predictions_24hr.png"))
plt.close()

##############################
# ===== PM10 Prediction =====
##############################
X_pm10 = df[features]
y_pm10 = df["pm10"]
X_train_p10, X_test_p10, y_train_p10, y_test_p10 = train_test_split(X_pm10, y_pm10, test_size=0.2, random_state=42)

model_pm10 = RandomForestRegressor(n_estimators=100, random_state=42)
model_pm10.fit(X_train_p10, y_train_p10)
y_pred_p10 = model_pm10.predict(X_test_p10)

r2_p10 = r2_score(y_test_p10, y_pred_p10)
mse_p10 = mean_squared_error(y_test_p10, y_pred_p10)
cv_scores_p10 = cross_val_score(model_pm10, X_pm10, y_pm10, scoring="r2", cv=KFold(n_splits=5, shuffle=True, random_state=42))

# Classification

def categorize_pm10(pm10):
    if pm10 <= 50:
        return "Good"
    elif pm10 <= 100:
        return "Moderate"
    elif pm10 <= 250:
        return "Poor"
    elif pm10 <= 350:
        return "Unhealthy"
    elif pm10 <= 430:
        return "Severe"
    else:
        return "Hazardous"

# Save PM10 model & results
joblib.dump(model_pm10, os.path.join(MODEL_DIR, "rf_regressor_pm10.pkl"))
df_pm10 = pd.DataFrame({"Actual_PM10": y_test_p10.values, "Predicted_PM10": y_pred_p10})
df_pm10["Category"] = df_pm10["Predicted_PM10"].apply(categorize_pm10)
df_pm10.to_csv(PREDICTIONS_PATH_PM10, index=False)

# Plot PM10 for last 24 hours
df_recent_pm10 = df.tail(24)
y_recent_pm10 = model_pm10.predict(df_recent_pm10[features])

plt.figure(figsize=(10, 5))
plt.plot(df_recent_pm10["datetime"], df_recent_pm10["pm10"], label="Actual PM10", marker="o")
plt.plot(df_recent_pm10["datetime"], y_recent_pm10, label="Predicted PM10", marker="x")
plt.title("PM10 Prediction (Last 24 Hours)")
plt.xlabel("Datetime")
plt.ylabel("PM10 Concentration")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "rf_pm10_predictions_24hr.png"))
plt.close()

##############################
# ===== Print Summary =======
##############################
print("\n✅ Models trained, evaluated, classified, and visualized.")
print(f"PM2.5 → R²: {r2_p25:.4f}, MSE: {mse_p25:.2f}, CV Avg R²: {cv_scores_p25.mean():.4f}")
print(f"PM10 → R²: {r2_p10:.4f}, MSE: {mse_p10:.2f}, CV Avg R²: {cv_scores_p10.mean():.4f}")
