// File: src/App.js

import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Charts from "./pages/Charts";
import PowerBI from "./pages/PowerBI";


function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/charts" element={<Charts />} />
        <Route path="/powerbi" element={<PowerBI />} />
      </Routes>
    </Router>
  );
}

export default App;
