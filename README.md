# 🌍 Air Quality Prediction & Forecasting Platform

A full-stack AI-driven project to predict and forecast PM2.5 and PM10 levels using historical air pollution and weather data. The system provides insights via an interactive React dashboard and Power BI visualizations.

> 🛠️ Built with Python, Flask, scikit-learn, React.js, and Power BI  
> 🔗 Backend hosted on Render | Frontend hosted on Vercel  
> 📈 Designed for public awareness, smart city dashboards, and environmental insights

---

## 📌 Overview

This project helps monitor air quality in real time and forecast pollution levels over the next 48 hours. It uses real environmental parameters like gas concentrations and weather metrics to predict air pollutant levels. A React dashboard visualizes the forecasts and predictions, while Power BI is used for advanced analytics.

The project includes:
- Real-time + historical data collection
- Machine learning-based predictions
- Category classification (e.g., Good, Moderate, Unhealthy)
- 48-hour air quality forecasts
- Professional frontend dashboard
- Power BI integration (⚙️ in development)

---

## ✅ Features

### 🧠 Machine Learning Models
- Two **Random Forest Regressor** models trained:
  - One for **PM2.5**
  - One for **PM10**
- Features used:
  - Gas concentrations: CO, NO2, O3, SO2, NH3
  - Weather: Temperature, Humidity, Wind Speed
  - Time: Hour of day, Day of week
- Trained on 2 weeks of historical data from OpenWeatherMap

### 🏷️ Classification
- Both predicted and forecasted pollutant values are categorized into AQI labels:
  - Good, Moderate, Poor, Unhealthy, Severe, Hazardous
- Categorization logic adheres to standard Indian AQI subindices

### ⏱️ Forecasting (48 Hours)
- Uses OpenWeatherMap’s **Air Pollution Forecast API**
- Forecasts hourly values for PM2.5 and PM10 up to 48 hours ahead
- Saves data to `future_pollution_forecast.csv`
- Generates plots and category breakdowns

### 📈 Visualizations
- 24-hour plots for actual vs predicted PM2.5 and PM10
- 48-hour forecast graphs for both pollutants
- All plots saved as PNGs for reporting and dashboard use

---

## 🖥️ React Frontend Dashboard

**Deployed on Vercel:** [air-quality-prediction.vercel.app](https://air-quality-prediction-zeta.vercel.app/)

### Pages:
1. **Dashboard**:
   - Table with filter & sort
   - Category dropdown
   - Styled with neutral & professional colors
2. **Charts**:
   - Plot actual vs predicted (PM2.5, PM10)
   - Plot future forecast (48h)
   - Uses Recharts for visualization
3. **Power BI (📌 In Development)**:
   - Placeholder screen
   - Embed visuals from Power BI workspace (to be integrated)

### Tech Stack:
- React.js (with Hooks & Router)
- Tailwind CSS (custom theme)
- Axios for API requests
- Modular component-based design

---

## 🧪 API & Backend

**Deployed on Render:** [air-quality-api-render.onrender.com](https://air-quality-prediction-yqua.onrender.com)

### Flask API Endpoints:
- `/predict` – Accepts POST input for features, returns predicted PM2.5 + category
- `/forecast` – Returns JSON of 48-hour forecast with predicted values + AQI categories
- `/health` – Simple health check route
- All responses are CORS-enabled for React frontend

### Model & Data Scripts:
- `train_model.py` – Trains PM2.5 and PM10 models, generates predictions and graphs
- `forecast_pollution.py` – Fetches 48h forecasts and classifies
- `collect_historical_aqi.py` – Pulls 2 weeks of AQI data from OpenWeatherMap
- `fetch_openweather_data.py` – Pulls weather forecast data

---

## 📊 Power BI Dashboard (⚙️ Under Development)

- Power BI Desktop used to create:
  1. 48-hour forecast line graph for PM2.5 and PM10
  2. 24-hour Actual vs Predicted graphs
  3. Category-wise distribution bar charts
- CSVs used:
  - `future_pollution_forecast.csv`
  - `pm25_predictions.csv`
  - `pm10_predictions.csv`
- Integration into React (PowerBI.js) is pending embed permissions

---


