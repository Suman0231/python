from flask import Flask, render_template, request
import requests

app = Flask(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Predefined cities with their latitude and longitude
CITIES = {
    # "Berlin": {"lat": 52.52, "lon": 13.41},
    # "New York": {"lat": 40.71, "lon": -74.01},
    # "London": {"lat": 51.51, "lon": -0.13},
    # "Tokyo": {"lat": 35.68, "lon": 139.69},
    # "Paris": {"lat": 48.85, "lon": 2.35}
    "Kathmandu": {"lat": 27.72, "lon": 85.32},
    "Pokhara": {"lat": 28.21, "lon": 83.99},
    "Biratnagar": {"lat": 26.48, "lon": 87.27},
    "Lalitpur": {"lat": 27.67, "lon": 85.32},
    "Bharatpur": {"lat": 27.68, "lon": 84.43}
}


@app.route("/", methods=["GET", "POST"])
def index():
    forecast = None
    error = None
    selected_city = None

    if request.method == "POST":
        selected_city = request.form.get("city")
        city_coords = CITIES.get(selected_city)

        if city_coords:
            try:
                params = {
                    "latitude": city_coords["lat"],
                    "longitude": city_coords["lon"],
                    "hourly": "temperature_2m"
                }

                response = requests.get(BASE_URL, params=params)

                if response.status_code == 200:
                    data = response.json()
                    times = data["hourly"]["time"][:10]  # first 10 hours
                    temps = data["hourly"]["temperature_2m"][:10]

                    forecast = list(zip(times, temps))
                else:
                    error = "Error fetching weather data."

            except Exception as e:
                error = f"An error occurred: {e}"
        else:
            error = "City not found."

    return render_template(
        "index.html",
        cities=CITIES.keys(),
        forecast=forecast,
        error=error,
        selected_city=selected_city
    )


if __name__ == "__main__":
    app.run(debug=True)