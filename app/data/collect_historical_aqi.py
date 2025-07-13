# collect_historical_aqi.py (fetch ~2 weeks of historical data + real-time AQI)

import requests
import time
import pandas as pd
import os
from datetime import datetime, timedelta, timezone

API_KEY = "4532fc36b320a237f0dd40f12a2ffa04"
LAT, LON = 28.6139, 77.2090  # Delhi coords
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

all_data = []

# Use timezone-aware timestamps
now = int(datetime.now(timezone.utc).timestamp())
two_weeks_ago = now - 14 * 24 * 3600

# Fetch 14 days of historical hourly AQI data (max 5 days per call)
for start in range(two_weeks_ago, now, 5 * 24 * 3600):
    end = min(start + 5 * 24 * 3600, now)
    url = (
        f"http://api.openweathermap.org/data/2.5/air_pollution/history"
        f"?lat={LAT}&lon={LON}&start={start}&end={end}&appid={API_KEY}"
    )
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json().get("list", [])
        for entry in data:
            dt = datetime.fromtimestamp(entry["dt"], tz=timezone.utc)
            components = entry["components"]
            all_data.append({"datetime": dt, **components})
    time.sleep(1.2)

# Save historical
hist_df = pd.DataFrame(all_data)
hist_df.to_csv(os.path.join(OUTPUT_DIR, "historical_aqi_openweather.csv"), index=False)
print("✅ Historical AQI data (2 weeks) saved.")
