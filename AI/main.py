from flask import Flask
from flask_cors import CORS
from plant import bp_plant
from soil import bp_soil
from sensor import bp_sensor

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Welcome to the GrowGarden AI API!"

# Register blueprints
app.register_blueprint(bp_plant, url_prefix="")
app.register_blueprint(bp_soil, url_prefix="")
app.register_blueprint(bp_sensor, url_prefix="")

#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=False)
