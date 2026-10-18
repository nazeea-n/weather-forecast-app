# Weather App



![Weather app screenshot](weather.png)



A Flask web app that shows the current weather and a 5-day forecast for any place. Every search is saved in MySQL and shown as recent searches.

## Features
- Search any town, city or village
- Current temperature, feels-like, humidity and wind
- 5-day forecast
- Recent searches saved in MySQL (optional: without MySQL the weather still works)
- Page colors change with the weather

## Tech stack
Python, Flask, MySQL (PyMySQL), Open-Meteo API (no API key needed), HTML, CSS, JavaScript

## How to run
1. Clone this repository and open the folder.
2. `python -m venv venv`
3. `venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. Copy `config.example.py`, rename the copy to `config.py`, and put your MySQL password in it.
6. `python app.py`
7. Open http://127.0.0.1:5000

## Project structure
- `app.py`: Flask server and API routes
- `weather_service.py`: fetches data from Open-Meteo
- `db.py`: saves and reads search history in MySQL
- `templates/index.html`: the web page
- `config.example.py`: MySQL settings template
