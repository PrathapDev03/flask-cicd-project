
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = "1.0"
APP_NAME = "Zero Downtime Deployment Demo"


@app.route("/")
def home():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "message": "Welcome to Version 1",
        "status": "Stable",
        "deployment": "Blue"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION
    }), 200


@app.route("/version")
def version():
    return jsonify({
        "version": APP_VERSION
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
