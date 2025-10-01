from flask import Blueprint, jsonify
import threading, time, json
from serial import Serial
from serial.serialutil import SerialException

bp_sensor = Blueprint("sensor", __name__)

latest_data = {}
last_raw_line = None
port_name = "COM5"
baud_rate = 9600

def read_serial():
    """Background thread to continuously read sensor data."""
    global latest_data, last_raw_line
    while True:
        try:
            with Serial(port_name, baud_rate, timeout=1) as ser:
                print(f"Serial port opened: {port_name}")
                while True:
                    line = ser.readline().decode(errors="ignore").strip()
                    if not line or line == last_raw_line:
                        continue
                    last_raw_line = line
                    try:
                        new_data = json.loads(line)
                    except json.JSONDecodeError:
                        print("Failed to parse JSON:", line)
                        continue

                    sensor_data = {
                        "Temperature": new_data.get("Temperature"),
                        "Humidity": new_data.get("Humidity"),
                        "Nitrogen": new_data.get("Nitrogen"),
                        "Phosphorus": new_data.get("Phosphorus"),
                        "Potassium": new_data.get("Potassium"),
                        "pH": new_data.get("pH"),
                        "RainAnalog": new_data.get("RainAnalog"),
                    }

                    if any(latest_data.get(k) != sensor_data[k] for k in sensor_data):
                        latest_data = sensor_data
                        print("New sensor data:", latest_data)
        except SerialException as e:
            print("Serial port error:", e)
            time.sleep(5)  # retry after 5 seconds

# Start the serial reader in a daemon thread
thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

@bp_sensor.route("/get-sensor")
def get_sensor():
    return jsonify(latest_data if latest_data else {"status": "No data yet"})

@bp_sensor.route("/check")
def check():
    return jsonify({"success": True, "message": latest_data})
