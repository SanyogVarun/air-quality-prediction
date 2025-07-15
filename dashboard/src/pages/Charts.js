// File: src/pages/Charts.js

import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import "./charts.css";

// Format datetime like "Sun, 13 Jul, 05:00 pm"
const formatDate = (isoString) => {
  const date = new Date(isoString);
  return date.toLocaleString('en-GB', {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
};

const Charts = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/forecast`)
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error("Failed to load chart data:", err));
  }, []);

  return (
    <div className="charts-container">
      <h2>📊 Air Quality Forecast - Trends</h2>

      <div className="chart-box">
        <h3>PM2.5 Forecast</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="datetime" tickFormatter={formatDate} />
            <Tooltip labelFormatter={formatDate} />
            <YAxis />
            <Legend />
            <Line type="monotone" dataKey="pred_pm25" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-box">
        <h3>PM10 Forecast</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="datetime" tickFormatter={formatDate} />
            <Tooltip labelFormatter={formatDate} />
            <YAxis />
            <Legend />
            <Line type="monotone" dataKey="pred_pm10" stroke="#82ca9d" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Charts;
