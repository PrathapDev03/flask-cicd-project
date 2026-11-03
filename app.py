from flask import Flask, jsonify
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0")

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Flask CI/CD Pipeline!",
        "application": "Flask Demo Application",
        "version": APP_VERSION
    })

@app.route("/health")
def health():
    if os.getenv("SIMULATE_HEALTH_FAILURE") == "true":
        return jsonify({
            "status": "unhealthy"
        }), 500

    return jsonify({
        "status": "healthy",
        "application": "Flask Demo Application",
        "version": APP_VERSION
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)