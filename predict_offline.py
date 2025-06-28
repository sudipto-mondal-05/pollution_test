import pandas as pd
import joblib

print("📂 Loading data from CSV...")
df = pd.read_csv("data/aqi_weather_2024.csv")

city = input("🌆 Enter city to predict for: ").strip()

if city.lower() not in [c.lower() for c in df['city'].unique()]:
    print("❌ City not found in dataset.")
    exit()

city_df = df[df['city'].str.lower() == city.lower()].dropna()

X = city_df[['temp', 'humidity', 'wind_speed', 'pm2_5', 'pm10', 'no2', 'so2', 'o3']]

print("📦 Loading model...")
model = joblib.load(f"models/{city.lower()}_model.pkl")

predictions = model.predict(X)

city_df['predicted_aqi'] = predictions
print("\n📊 Sample Predictions:")
print(city_df[['date', 'aqi', 'predicted_aqi']].head(10))
