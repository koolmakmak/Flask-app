from flask import Flask, request, jsonify
from flask_cors import CORS
from plant import bp_plant
from soil import bp_soil
from sensor import bp_sensor
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

db_url = os.getenv("DATABASE_URL", "sqlite:///sensors.db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ldr = db.Column(db.Float, nullable=True)
    rain_analog = db.Column(db.Float, nullable=True)
    rain_digital = db.Column(db.Integer, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    soil_temp = db.Column(db.Float, nullable=True)
    moisture = db.Column(db.Float, nullable=True)
    ec = db.Column(db.Float, nullable=True)
    ph = db.Column(db.Float, nullable=True)
    nitrogen = db.Column(db.Float, nullable=True)
    phosphorus = db.Column(db.Float, nullable=True)
    potassium = db.Column(db.Float, nullable=True)
    salinity = db.Column(db.Float, nullable=True)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Welcome to the GrowGarden AI API with Database!"

@app.route("/api/sensor", methods=["POST"])
def receive_sensor():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Invalid JSON"}), 400

        record = SensorData(
            ldr=data.get("LDR"),
            rain_analog=data.get("RainAnalog"),
            rain_digital=data.get("RainDigital"),
            humidity=data.get("Humidity"),
            temperature=data.get("Temperature"),
            soil_temp=data.get("SoilTemp"),
            moisture=data.get("Moisture"),
            ec=data.get("EC"),
            ph=data.get("pH"),
            nitrogen=data.get("Nitrogen"),
            phosphorus=data.get("Phosphorus"),
            potassium=data.get("Potassium"),
            salinity=data.get("Salinity"),
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({"success": True, "message": "Data saved", "id": record.id}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/sensor/latest", methods=["GET"])
def get_latest_sensor():
    record = SensorData.query.order_by(SensorData.id.desc()).first()
    if not record:
        return jsonify({"success": False, "message": "No data yet"}), 404

    return jsonify({
        "success": True,
        "data": {
            "id": record.id,
            "LDR": record.ldr,
            "RainAnalog": record.rain_analog,
            "RainDigital": record.rain_digital,
            "Humidity": record.humidity,
            "Temperature": record.temperature,
            "SoilTemp": record.soil_temp,
            "Moisture": record.moisture,
            "EC": record.ec,
            "pH": record.ph,
            "Nitrogen": record.nitrogen,
            "Phosphorus": record.phosphorus,
            "Potassium": record.potassium,
            "Salinity": record.salinity,
        }
    }), 200

app.register_blueprint(bp_plant, url_prefix="")
app.register_blueprint(bp_soil, url_prefix="")
app.register_blueprint(bp_sensor, url_prefix="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
