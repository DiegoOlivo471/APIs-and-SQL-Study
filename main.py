import sys
from iss.iss import fetch_iss_data, get_iss_position, get_iss_timestamp
from weather.weather import fetch_weather_data, get_weather_summary
from database.db import create_table, insert_record

# Fetching the data.
iss_data = fetch_iss_data()
if iss_data is None:
    print("Não foi possível obter dados da ISS.")
    sys.exit(1)

iss_data_timestamp = get_iss_timestamp(iss_data)
position = get_iss_position(iss_data)

weather_data = fetch_weather_data(position["latitude"], position["longitude"])
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