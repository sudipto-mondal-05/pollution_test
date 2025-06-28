import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

print("📊 Loading data...")

# Load dataset
df = pd.read_csv("data/aqi_weather_2024.csv")
df.columns = df.columns.str.strip()

# Drop rows with missing values
df = df.dropna(subset=['temp', 'humidity', 'wind_speed', 'cloud_cover', 'aqi'])

X = df[['temp', 'humidity', 'wind_speed', 'cloud_cover']]
y = df['aqi']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # Fixed line
r2 = r2_score(y_test, y_pred)

print(f"✅ RMSE: {rmse:.2f}")
print(f"📈 R² Score: {r2:.2f}")

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/aqi_model.pkl")
print("📦 Saved model: models/aqi_model.pkl")
