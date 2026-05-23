from flask import Flask, request, render_template, jsonify
from data_loader import get_single_city_data
from graphs import generate_city_graph
import pandas as pd
import requests

app = Flask(__name__)

API_KEY = "YOUR_OPENWEATHER_API_KEY"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result")
def result():
    city = request.args.get("city")
    date = request.args.get("date")

    df = get_single_city_data(city)

    if df is None or df.empty:
        return render_template("result.html", error="City data not found")

    full_df = df.copy()

    last_date = full_df['Date'].max()

    if date:
        selected_date = pd.to_datetime(date)

        if selected_date > last_date:
            return render_template("result.html", error="Prediction not included in this version")

        match = full_df[full_df['Date'].dt.date == selected_date.date()]

        if match.empty:
            return render_template("result.html", error="No data for selected date")

        data = match.iloc[0].to_dict()

    else:
        data = full_df.iloc[-1].to_dict()

    graph = generate_city_graph(city)

    return render_template(
        "result.html",
        city=city,
        data=data,
        graph=graph
    )


@app.route("/aqi")
def aqi():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City required"}), 400

    geo = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    ).json()

    if not geo:
        return jsonify({"error": "City not found"}), 400

    lat, lon = geo[0]["lat"], geo[0]["lon"]

    data = requests.get(
        f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    ).json()

    return jsonify({
        "city": city,
        "aqi": data["list"][0]["main"]["aqi"] * 50,
        "pm25": data["list"][0]["components"]["pm2_5"],
        "pm10": data["list"][0]["components"]["pm10"],
        "ozone": data["list"][0]["components"].get("o3", 0)
    })


if __name__ == "__main__":
    app.run(debug=True)
