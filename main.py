import sys
from iss.iss import fetch_iss_data, get_iss_position, get_iss_timestamp
from weather.weather import fetch_weather_data, get_weather_summary
from database.db import create_table, insert_record
import time 

tries_iss = 0
tries_weather = 0
while True:
    # Fetching the data.
    while True:
        iss_data = fetch_iss_data()
        if iss_data is not None:
            break
        tries_iss += 1
        if tries_iss >= 3:
            print("Could not fetch ISS data after 3 tries.")
            sys.exit(1)
        print(f"Retrying to fetch ISS data... ({tries_iss}/3)")
        time.sleep(10)  # Waits 10 seconds and try again, maximum of 3 tries before quitting.
    tries_iss = 0
    
    iss_data_timestamp = get_iss_timestamp(iss_data)
    position = get_iss_position(iss_data)

    while True:
        weather_data = fetch_weather_data(position["latitude"], position["longitude"])
        if weather_data is not None:
            break
        tries_weather += 1
        if tries_weather >= 3:
            print("Could not fetch OpenWeatherMap data after 3 tries.")
            sys.exit(1)
        print(f"Retrying to fetch OpenWeatherMap data... ({tries_weather}/3)")
        time.sleep(10)
    tries_weather = 0

    summ = get_weather_summary(weather_data)

    # Structuring the data to fit the database.
    values = (iss_data_timestamp,
            position["latitude"],
            position["longitude"],
            summ["country"],
            summ["temp"],
            summ["feels_like"],
            summ["humidity"],
            summ["condition"]["main"],
            summ["wind"]["speed"]
            )

    create_table()
    insert_record(values)

    time.sleep(300)  # Waits 5 minutes for the next requests.