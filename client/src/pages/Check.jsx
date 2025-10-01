import React, { useState, useEffect } from "react";
import "./Check.css";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const GoHomeButton = ({ onClick }) => (
  <button className="advice-title" onClick={onClick}>
    ← Back
  </button>
);

const CropPredictor = ({ sensorData }) => {
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const predictCrop = async () => {
    if (!sensorData) {
      setError("Sensor data not loaded yet.");
      setPrediction(null);
      return;
    }

    try {
      setError(null);
      const res = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          n: sensorData.Nitrogen || 0,
          p: sensorData.Phosphorus || 0,
          k: sensorData.Potassium || 0,
          temp: sensorData.Temperature || 0,
          hum: sensorData.Humidity || 0,
          ph_val: sensorData.pH || 0,
          rain: sensorData.RainAnalog || 0,
        }),
      });

      const data = await res.json();

      if (data.error) {
        setError(data.error);
        setPrediction(null);
      } else {
        setPrediction(data.crop);
      }
    } catch {
      setError("❌ Failed to predict crop. Please check server.");
      setPrediction(null);
    }
  };

  return (
    <div>
      <button className="predict-button" onClick={predictCrop}>
        Predict Crop from Sensor Data
      </button>

      {prediction && (
        <p className="prediction-result">
          🌱 <strong>Recommended crop:</strong> {prediction}
        </p>
      )}

      {error && <p className="error-text">{error}</p>}
    </div>
  );
};

const SoilPredictor = ({ sensorData }) => {
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const predictSoil = async () => {
    if (!sensorData) {
      setError("Sensor data not loaded yet.");
      setPrediction(null);
      return;
    }

    try {
      setError(null);
      const res = await fetch("http://localhost:4000/wish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          pH: sensorData.pH || 0,
          EC: sensorData.EC || 0,
          N: sensorData.Nitrogen || 0,
          P: sensorData.Phosphorus || 0,
          K: sensorData.Potassium || 0,
        }),
      });

      const data = await res.json();

      if (data.error) {
        setError(data.error);
        setPrediction(null);
      } else {
        setPrediction(data.crop);
      }
    } catch {
      setError("❌ Failed to predict soil. Please check server.");
      setPrediction(null);
    }
  };

  return (
    <div>
      <button className="predict-button" onClick={predictSoil}>
        Predict Soil from Sensor Data
      </button>

      {prediction && (
        <p className="prediction-result">
          🌱 <strong>Recommended soil:</strong> {prediction}
        </p>
      )}

      {error && <p className="error-text">{error}</p>}
    </div>
  );
};

const Check = () => {
  const navigate = useNavigate();
  const [sensorData, setSensorData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:3000/get-sensor");
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        setSensorData(data);
        console.log(`FROM CHECK: ${data.Temperature}`);
      } catch (error) {
        console.error("Failed to fetch sensor data", error);
        setSensorData(null);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      transition={{ duration: 0.5 }}
    >
      <div className="advice-container">
        <GoHomeButton onClick={() => navigate("/")} />

        <div className="advice-card">
          <h1>🌿 Crop Advice</h1>
          <p className="intro">
            Based on your soil and climate conditions, we recommend the following crops:
          </p>

          <div style={{ marginTop: "20px" }}>
            <CropPredictor sensorData={sensorData} />
          </div>

          <div style={{ marginTop: "20px" }}>
            <SoilPredictor sensorData={sensorData} />
          </div>

          <div style={{ marginTop: "20px" }}>
            <h3>Current Sensor Data:</h3>

            {!sensorData && (
              <p className="error-text">❌ Failed to load sensor data. Please check connection.</p>
            )}

            {sensorData && (
              <>
                {sensorData.is_stale && (
                  <p style={{ color: "orange" }}>
                    ⚠ Data may be outdated (last update {sensorData.last_update_seconds || "?"} seconds ago)
                  </p>
                )}

                <div className="sensor-grid">
                  <div>🌡 Temperature: <strong>{sensorData.Temperature} °C</strong></div>
                  <div>💧 Humidity: <strong>{sensorData.Humidity} %</strong></div>
                  <div>🌱 Nitrogen: <strong>{sensorData.Nitrogen}</strong></div>
                  <div>⚡ Phosphorus: <strong>{sensorData.Phosphorus}</strong></div>
                  <div>🪵 Potassium: <strong>{sensorData.Potassium}</strong></div>
                  <div>⚗ pH: <strong>{sensorData.pH}</strong></div>
                  <div>🌧 Rain: <strong>{sensorData.RainAnalog}</strong></div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default Check;
