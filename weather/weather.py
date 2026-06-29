import os
from dotenv import load_dotenv, dotenv_values
import requests
from requests.exceptions import HTTPError
import pycountry

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(lat, lon):
    """
    Fetches raw weather data from the API, using the current weather endpoint url
    """
    url = f"{WEATHER_BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Sucess:", response.json())
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error ocurred: {http_err}")
    except Exception as err:
        print(f"Other error ocurred: {err}")

def get_temperature_data(weather_data):
    """
    Returns temperature-related fields: temp, feels_like, temp_min, temp_max, humidity
    """
    temp_data = weather_data.get("main").copy()
    temp_data.pop("sea_level", None)
    temp_data.pop("grnd_level", None)
    return temp_data

def get_weather_condition(weather_data):
    """
    Returns the weather type and description
    """
    cond = weather_data.get("weather")
    return {"main": cond[0].get("main"), "description": cond[0].get("description")}

def get_location_data(weather_data):
    """
    Returns the country code
    """
    country_code = weather_data.get("sys", {}).get("country")
    
    if not country_code:
      return None
    
    country = pycountry.countries.get(alpha_2=country_code)
    return country.name if country else None

def get_wind_data(weather_data):
    """
    Returns wind speed
    """
    return weather_data.get("wind")

def get_weather_summary(weather_data):
    """
    Returns a consolidated dict with all relevant weather information
    """
    summary = {}
    summary.update(get_temperature_data(weather_data))
    summary["condition"] = get_weather_condition(weather_data)
    summary["country"] = get_location_data(weather_data)
    summary["wind"] = get_wind_data(weather_data)
    return summary