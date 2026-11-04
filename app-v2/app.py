
from flask import Flask, jsonify
import os

app = Flask(__name__)

APP_VERSION = "2.0"
APP_NAME = "Zero Downtime Deployment Demo"

# Controlled failure simulation
SIMULATE_FAILURE = os.getenv(
    "SIMULATE_FAILURE", "false"
).lower() == "true"


@app.route("/")
def home():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "message": "Welcome to Version 2",
        "status": "New Release",
        "deployment": "Green",
        "features": [
            "Improved application response",
            "Blue-Green deployment support",
            "Automated rollback support"
        ]
    })


@app.route("/health")
def health():

    if SIMULATE_FAILURE:
        return jsonify({
            "status": "unhealthy",
            "version": APP_VERSION,
            "message": "Simulated deployment failure"
        }), 503

    return jsonify({
        "status": "healthy",
        "version": APP_VERSION
    }), 200


@app.route("/version")
def version():
    return jsonify({
        "version": APP_VERSION,
        "deployment": "Green"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
