import requests
from flask import Flask, jsonify, render_template, request

import db
import weather_service as ws

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify(error="Please enter a city name"), 400
    try:
        data = ws.get_weather(city)
    except ws.CityNotFound:
        return jsonify(error=f"City '{city}' not found"), 404
    except requests.RequestException:
        return jsonify(error="Could not reach the weather service. Check your internet."), 502

    cur = data["current"]
    db.save_search(data["city"], data["country"], cur["temperature"], cur["description"])
    return jsonify(data)


@app.get("/api/history")
def history():
    rows = db.get_history()
    if rows is None:
        return jsonify(available=False, history=[])
    return jsonify(available=True, history=rows)


if __name__ == "__main__":
    app.run(debug=True)
