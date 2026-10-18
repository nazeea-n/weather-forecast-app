"""Talks to the free Open-Meteo API (no API key needed)."""
import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather codes used by Open-Meteo -> (description, emoji)
CODES = {
    0: ("Clear sky", "☀️"),
    1: ("Mostly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Drizzle", "🌦️"),
    55: ("Heavy drizzle", "🌦️"),
    61: ("Light rain", "🌧️"),
    63: ("Rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    71: ("Light snow", "🌨️"),
    73: ("Snow", "🌨️"),
    75: ("Heavy snow", "❄️"),
    80: ("Light showers", "🌦️"),
    81: ("Showers", "🌧️"),
    82: ("Heavy showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with hail", "⛈️"),
    99: ("Thunderstorm with hail", "⛈️"),
}


class CityNotFound(Exception):
    pass


def describe(code):
    return CODES.get(code, ("Unknown", "❓"))


def find_city(name):
    """Turn a city name into latitude and longitude."""
    r = requests.get(GEO_URL, params={"name": name, "count": 1, "language": "en"}, timeout=10)
    r.raise_for_status()
    results = r.json().get("results")
    if not results:
        raise CityNotFound(name)
    c = results[0]
    return {
        "name": c["name"],
        "country": c.get("country", ""),
        "latitude": c["latitude"],
        "longitude": c["longitude"],
    }


def get_weather(city_name):
    """Return current weather and a 5-day forecast for a city."""
    city = find_city(city_name)
    r = requests.get(FORECAST_URL, params={
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 5,
    }, timeout=10)
    r.raise_for_status()
    data = r.json()

    cur = data["current"]
    text, icon = describe(cur["weather_code"])
    daily = data["daily"]
    days = []
    for i, date in enumerate(daily["time"]):
        d_text, d_icon = describe(daily["weather_code"][i])
        days.append({
            "date": date,
            "max": daily["temperature_2m_max"][i],
            "min": daily["temperature_2m_min"][i],
            "rain": daily["precipitation_sum"][i],
            "description": d_text,
            "icon": d_icon,
        })
    return {
        "city": city["name"],
        "country": city["country"],
        "current": {
            "temperature": cur["temperature_2m"],
            "feels_like": cur["apparent_temperature"],
            "humidity": cur["relative_humidity_2m"],
            "wind": cur["wind_speed_10m"],
            "description": text,
            "icon": icon,
        },
        "daily": days,
    }
