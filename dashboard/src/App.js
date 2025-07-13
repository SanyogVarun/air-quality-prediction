import React, { useEffect, useState } from "react";
import { fetchForecastData } from "./api";
import "./App.css";

function App() {
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      const data = await fetchForecastData();
      if (data) {
        setForecast(data.forecast || []);
      }
      setLoading(false);
    }
    loadData();
  }, []);

  return (
    <div className="App">
      <h1>🌍 Air Quality Forecast</h1>
      {loading ? (
        <p>Loading forecast...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Datetime</th>
              <th>PM2.5</th>
              <th>Category</th>
              <th>PM10</th>
              <th>Category</th>
            </tr>
          </thead>
          <tbody>
            {forecast.slice(0, 20).map((item, index) => (
              <tr key={index}>
                <td>{new Date(item.datetime).toLocaleString()}</td>
                <td>{item.pred_pm25.toFixed(1)}</td>
                <td>{item.cat_pm25}</td>
                <td>{item.pred_pm10.toFixed(1)}</td>
                <td>{item.cat_pm10}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
