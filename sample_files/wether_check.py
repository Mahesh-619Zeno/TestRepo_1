import os
import sys
import logging
import requests
from datetime import datetime

# ------------------------------
# Load Configuration from Environment
# ------------------------------
APP_ENV = os.getenv("APP_ENV", "dev")
API_KEY = os.getenv("WEATHER_API_KEY")
ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "false").lower() == "true"
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "New York")

# ------------------------------
# Setup Logging
# ------------------------------
if ENABLE_LOGGING:
    logging.basicConfig(
        level=logging.DEBUG if APP_ENV == "dev" else logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

# ------------------------------
# Utility Functions
# ------------------------------
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': API_KEY
    }

    if not API_KEY:
        logger.error("Missing WEATHER_API_KEY.")
        raise ValueError("API key not set.")

    try:
        logger.debug(f"Requesting weather for {city_name}")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

def print_weather_info(data):
    if not data:
        print("No weather data available.")
        return

    try:
        city = data['name']
        country = data['sys']['country']
        temp = kelvin_to_celsius(data['main']['temp'])
        weather = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        timestamp = data['dt']
        time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        print("\n--- Weather Report ---")
        print(f"Environment : {APP_ENV.upper()}")
        print(f"Location    : {city}, {country}")
        print(f"Time        : {time}")
        print(f"Temperature : {temp:.2f}°C")
        print(f"Weather     : {weather.capitalize()}")
        print(f"Humidity    : {humidity}%")
        print(f"Wind Speed  : {wind_speed} m/s")
        print("----------------------\n")
    except KeyError as e:
        logger.error(f"Missing data field: {e}")
        print("Failed to display weather info.")

# ------------------------------
# Main CLI
# ------------------------------
def run():
    print(f"Running in '{APP_ENV}' environment.")
    
    city = input(f"Enter city name (or press Enter for default: {DEFAULT_CITY}): ").strip()
    if not city:
        city = DEFAULT_CITY

    logger.info(f"Using city: {city}")
    data = get_weather(city)
    print_weather_info(data)

# ------------------------------
# Entry Point
# ------------------------------
if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logger.exception("Application error.")
        sys.exit(1)