// File: src/pages/PowerBI.js

import React from "react";
import "./powerbi.css";

const PowerBI = () => {
  return (
    <div className="powerbi-container">
      <h2>📈 Power BI Visualizations</h2>
      <div className="powerbi-embed">
        <iframe
          title="Air Quality Power BI Report"
          width="100%"
          height="600px"
          src="https://app.powerbi.com/view?r=YOUR_EMBED_URL"
          allowFullScreen
        ></iframe>
      </div>
    </div>
  );
};

export default PowerBI;
