import requests
from datetime import datetime

ISS_BASE_URL = "http://api.open-notify.org"
ISS_POSITION_ENDPOINT = f"{ISS_BASE_URL}/iss-now.json"
ASTRONAUTS_ENDPOINT = f"{ISS_BASE_URL}/astros.json"

def fetch_iss_data():
    """
    Fetches raw ISS position and timestamp datas from the API
    """
    response_iss = requests.get(ISS_POSITION_ENDPOINT)
    return response_iss.json()

def fetch_astronauts_data():
    """
    Fetches raw astronauts data from the API
    """
    response_astronauts = requests.get(ASTRONAUTS_ENDPOINT)
    return response_astronauts.json()

def get_iss_position(iss_data):
    """
    Returns the current International Space Station longitude and latitude
    """
    return iss_data.get("iss_position")

def get_iss_timestamp(iss_data):
    """
    Returns the current timestamp, converted to datetime (YEAR-MONTH-DAY HOUR-MINUTE-SECONDS)
    """
    current_timestamp = iss_data.get("timestamp")
    return datetime.fromtimestamp(current_timestamp)

def get_astronauts(astronauts_data):
    """
    Returns a list with the names of all the astronauts in space
    """
    return [astronaut["name"] for astronaut in astronauts_data.get("people")]

def get_astronauts_crafts(astronauts_data):
    """
    Returns a dict with the names of the astronauts in each craft

    Returns:
    dict: A dictionary containing:
        - 'craft' (str): The craft.
        - 'number' (int): The number of people in said craft.
    """
    crafts = {}
    for astronaut in astronauts_data.get("people"):
        crafts.setdefault(astronaut["craft"], 0)
        crafts[astronaut["craft"]] += 1
    return crafts

def get_astronauts_number(astronauts_data):
    """
    Returns the number of astronauts currently in space
    """
    return astronauts_data.get("number")