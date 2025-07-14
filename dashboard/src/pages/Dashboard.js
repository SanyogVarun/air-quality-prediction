import React, { useEffect, useState } from 'react';
import './dashboard.css';

function App() {
  const [data, setData] = useState([]);
  const [pm25Filter, setPm25Filter] = useState('All');
  const [pm10Filter, setPm10Filter] = useState('All');

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/forecast`)
      .then((res) => res.json())
      .then((result) => setData(result))
      .catch((err) => console.error('Error fetching data:', err));
  }, []);

  const filteredData = data.filter((row) => {
    return (pm25Filter === 'All' || row.cat_pm25 === pm25Filter) &&
           (pm10Filter === 'All' || row.cat_pm10 === pm10Filter);
  });

  const uniquePM25 = [...new Set(data.map(item => item.cat_pm25))];
  const uniquePM10 = [...new Set(data.map(item => item.cat_pm10))];

  return (
    <div className="container">
      <h1>Air Quality Forecast Dashboard</h1>

      <div className="controls">
        <div>
          <label>PM2.5 Category:</label>{' '}
          <select value={pm25Filter} onChange={(e) => setPm25Filter(e.target.value)}>
            <option value="All">All</option>
            {uniquePM25.map((cat, i) => (
              <option key={i} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <div>
          <label>PM10 Category:</label>{' '}
          <select value={pm10Filter} onChange={(e) => setPm10Filter(e.target.value)}>
            <option value="All">All</option>
            {uniquePM10.map((cat, i) => (
              <option key={i} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Date & Time</th>
            <th>PM2.5 (μg/m³)</th>
            <th>PM2.5 Category</th>
            <th>PM10 (μg/m³)</th>
            <th>PM10 Category</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.length > 0 ? (
            filteredData.map((row, index) => (
              <tr key={index}>
                <td>{new Date(row.datetime).toLocaleString('en-IN', {
                  weekday: 'short',
                  hour: '2-digit',
                  minute: '2-digit',
                  day: 'numeric',
                  month: 'short'
                })}</td>
                <td>{row.pred_pm25.toFixed(1)}</td>
                <td>{row.cat_pm25}</td>
                <td>{row.pred_pm10.toFixed(1)}</td>
                <td>{row.cat_pm10}</td>
              </tr>
            ))
          ) : (
            <tr><td colSpan="5">No forecast data available.</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default App;
