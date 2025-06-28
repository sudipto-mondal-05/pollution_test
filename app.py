# app.py

import streamlit as st
import joblib
import requests
import datetime
import pandas as pd

st.set_page_config(page_title="Live AQI Predictor", layout="centered")
st.title("🌫️ Live AQI Predictor")
st.markdown("Predict air quality using live weather + cloud data.")

# Load trained model
model = joblib.load("models/aqi_model.pkl")

# User input: City
city = st.text_input("📍 Enter your city name", "Hisar")

# Get today's date
today = datetime.date.today()

# Fetch weather + cloud data from Open-Meteo
@st.cache_data(ttl=3600)
def get_weather_data(city_name):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        geo_resp = requests.get(geo_url).json()

        if not geo_resp.get("results"):
            return None

        lat = geo_resp["results"][0]["latitude"]
        lon = geo_resp["results"][0]["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,"
            f"wind_speed_10m,cloud_cover"
        )
        weather_data = requests.get(weather_url).json()
        current = weather_data.get("current", {})

        return {
            "temp": current.get("temperature_2m", 0),
            "humidity": current.get("relative_humidity_2m", 0),
            "wind_speed": current.get("wind_speed_10m", 0),
            "cloud_cover": current.get("cloud_cover", 0),
        }

    except Exception:
        return None

# Fetch weather
weather = get_weather_data(city)

# Display and predict
if weather:
    st.success("✅ Live Weather Data Fetched")
    st.write(weather)

    # Format input as DataFrame
    input_df = pd.DataFrame([weather])
    aqi_pred = model.predict(input_df)[0]

    st.subheader("🌍 Predicted AQI:")
    st.metric("AQI", f"{int(aqi_pred)}")

    # AQI status labels
    if aqi_pred <= 50:
        st.success("Air Quality: Good 😊")
    elif aqi_pred <= 100:
        st.info("Air Quality: Satisfactory 😐")
    elif aqi_pred <= 200:
        st.warning("Air Quality: Moderate 😷")
    elif aqi_pred <= 300:
        st.error("Air Quality: Poor 😵")
    elif aqi_pred <= 400:
        st.error("Air Quality: Very Poor ☠️")
    else:
        st.error("Air Quality: Severe 🧨")

else:
    st.error("❌ Could not fetch weather data. Please check the city name or try again.")
