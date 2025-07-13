// File: src/components/Navbar.js

import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-title">🌍 Air Quality Predictor By SV </div>
      <div className="navbar-links">
        <Link to="/" className={location.pathname === "/" ? "active" : ""}>
          Dashboard
        </Link>
        <Link to="/charts" className={location.pathname === "/charts" ? "active" : ""}>
          Charts
        </Link>
        <Link to="/powerbi" className={location.pathname === "/powerbi" ? "active" : ""}>
          Power BI
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
