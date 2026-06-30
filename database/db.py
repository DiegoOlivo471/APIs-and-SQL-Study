import sqlite3

DB_NAME = "weather_history.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            latitude REAL,
            longitude REAL,
            country TEXT,
            temp REAL,
            feels_like REAL,
            humidity INTEGER,
            condition_main TEXT,
            wind_speed REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_record(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO registros (timestamp, latitude, longitude, country, temp, feels_like, humidity, condition_main, wind_speed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
        # data["timestamp"], data["latitude"], data["longitude"], data["country"],
        # data["temp"], data["feels_like"], data["humidity"], data["condition_main"], data["wind_speed"]
    conn.commit()
    conn.close()