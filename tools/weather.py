import requests

DESCRIPTION = """weather: Get current weather for any city. Uses Open-Meteo (free, no API key).
Input: {"city": "city name"}
Example: {"city": "Mumbai"}, {"city": "London"}"""

WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy fog", 51: "Light drizzle", 53: "Moderate drizzle",
    61: "Light rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Light snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Light showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail",
}

def weather(params: dict) -> str:
    city = params.get("city", "").strip()
    if not city:
        return "Error: No city provided."
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}, timeout=10
        ).json()
        if not geo.get("results"):
            return f"City '{city}' not found."

        loc = geo["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        name, country = loc["name"], loc.get("country", "")

        w = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weathercode",
                "temperature_unit": "celsius"
            }, timeout=10
        ).json()

        c = w["current"]
        condition = WMO_CODES.get(c["weathercode"], f"Code {c['weathercode']}")
        return (
            f"Weather in {name}, {country}:\n"
            f"  Condition   : {condition}\n"
            f"  Temperature : {c['temperature_2m']}°C\n"
            f"  Humidity    : {c['relative_humidity_2m']}%\n"
            f"  Wind Speed  : {c['wind_speed_10m']} km/h"
        )
    except Exception as e:
        return f"Weather Error: {e}"