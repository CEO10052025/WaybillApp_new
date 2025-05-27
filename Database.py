import sqlite3
from pathlib import Path

def init_db(db_file: str = "data/waybills.db"):
    Path(db_file).parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS Drivers(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        license TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Vehicles(
        id INTEGER PRIMARY KEY,
        plate TEXT NOT NULL,
        model TEXT,
        type TEXT,
        mileage INTEGER
    );
    CREATE TABLE IF NOT EXISTS Routes(
        id INTEGER PRIMARY KEY,
        start TEXT,
        end TEXT,
        distance INTEGER,
        route_type TEXT
    );
    CREATE TABLE IF NOT EXISTS Waybills(
        id INTEGER PRIMARY KEY,
        date TEXT,
        driver_id INTEGER,
        vehicle_id INTEGER,
        route_id INTEGER,
        mileage_start INTEGER,
        mileage_end INTEGER,
        fuel REAL,
        FOREIGN KEY(driver_id) REFERENCES Drivers(id),
        FOREIGN KEY(vehicle_id) REFERENCES Vehicles(id),
        FOREIGN KEY(route_id) REFERENCES Routes(id)
    );
    """)
    conn.commit()
    conn.close()
