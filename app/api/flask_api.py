from flask import Flask, request, jsonify, Response
from flask_cors import CORS  # ✅ Import CORS
import joblib
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

# Paths
BASE = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE, "../model")
OUTPUT_DIR = os.path.join(BASE, "../data/output")
FORECAST_CSV = os.path.join(OUTPUT_DIR, "future_pollution_forecast.csv")

# Load models
pm25_path = os.path.join(MODEL_DIR, "rf_regressor_pm25.pkl")
pm10_path = os.path.join(MODEL_DIR, "rf_regressor_pm10.pkl")

for p in [pm25_path, pm10_path]:
    if not os.path.exists(p):
        raise FileNotFoundError(f"Model not found: {p}")

pm25_model = joblib.load(pm25_path)
pm10_model = joblib.load(pm10_path)

# Categorization functions
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

# Root route
@app.route("/", methods=["GET"])
def index():
    return (
        "🌍 Air Quality Prediction API is running. "
        "Use POST /predict or GET /forecast or GET /health",
        200
    )

# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "API is healthy ✅"}), 200

# Prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    required = ["co", "no2", "o3", "so2", "nh3", "temperature", "humidity", "wind_speed", "hour", "dayofweek"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    X = [[data[k] for k in required]]
    pred25 = float(pm25_model.predict(X)[0])
    pred10 = float(pm10_model.predict(X)[0])

    return jsonify({
        "pm2_5": round(pred25, 2),
        "pm2_5_category": categorize_pm25(pred25),
        "pm10": round(pred10, 2),
        "pm10_category": categorize_pm10(pred10)
    }), 200

# Forecast endpoint
@app.route("/forecast", methods=["GET"])
def forecast():
    if not os.path.exists(FORECAST_CSV):
        return jsonify({"error": "Forecast not available"}), 404

    df = pd.read_csv(FORECAST_CSV, parse_dates=["datetime"])
    return Response(df.to_json(orient="records", date_format="iso"),
                    mimetype="application/json"), 200

if __name__ == "__main__":
    app.run(debug=True)
