# fetch_openweather_data.py (enhanced for forecast and historical weather)

import requests
import pandas as pd
import os
from datetime import datetime

API_KEY = "4532fc36b320a237f0dd40f12a2ffa04"
CITY = "Delhi"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Real-time + forecast weather data (5-day)
forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
response = requests.get(forecast_url)
data = response.json()

records = []
for item in data["list"]:
    dt = datetime.fromtimestamp(item["dt"])
    main = item["main"]
    wind = item.get("wind", {})
    records.append({
        "datetime": dt,
        "temperature": main.get("temp"),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "source": "forecast"
    })

forecast_df = pd.DataFrame(records)
forecast_df.to_csv(os.path.join(OUTPUT_DIR, "forecast_weather.csv"), index=False)
print("✅ Forecast weather data saved.")