# fetch_weather.py

import pandas as pd
import requests
from tqdm import tqdm
import time

# Load AQI data
aqi_df = pd.read_csv("data/raw_aqi.csv")

# Define Hisar coordinates
latitude = 29.1482
longitude = 75.7366

# Prepare output
weather_data = []

print("⏳ Fetching weather data from Open-Meteo...")
for index, row in tqdm(aqi_df.iterrows(), total=len(aqi_df)):
    date = row['date']
    aqi = row['aqi']

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}&longitude={longitude}"
        f"&start_date={date}&end_date={date}"
        f"&hourly=temperature_2m,relative_humidity_2m,windspeed_10m,cloudcover"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url)
        data = response.json()

        # Extract average of 24 hourly values
        weather = {
            "date": date,
            "temp": sum(data["hourly"]["temperature_2m"]) / 24,
            "humidity": sum(data["hourly"]["relative_humidity_2m"]) / 24,
            "wind_speed": sum(data["hourly"]["windspeed_10m"]) / 24,
            "cloud_cover": sum(data["hourly"]["cloudcover"]) / 24,
            "aqi": aqi
        }
        weather_data.append(weather)
        time.sleep(0.1)  # prevent rate limiting
    except Exception as e:
        print(f"⚠️ Failed on {date}: {e}")

# Save the enriched dataset
df_out = pd.DataFrame(weather_data)
df_out.to_csv("data/aqi_weather_2024.csv", index=False)
print("✅ Saved enriched data to data/aqi_weather_2024.csv")
