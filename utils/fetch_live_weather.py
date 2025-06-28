import requests
from datetime import datetime

def fetch_live_weather(api_key, location="Hisar,India"):
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{today}?unitGroup=metric&key={api_key}&include=days"

    print("🌤️ Fetching weather...")
    try:
        response = requests.get(url)
        data = response.json()

        day = data['days'][0]
        return {
            "temp": day['temp'],
            "humidity": day['humidity'],
            "wind_speed": day['windspeed'],
            "cloud_cover": day['cloudcover']
        }
    except Exception as e:
        print("❌ Weather fetch failed:", e)
        return None
