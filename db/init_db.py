import sqlite3
import os

dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(dir, "gateway.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
                CREATE TABLE IF NOT EXISTS meters (
                    meter_id NVARCHAR(36) PRIMARY KEY,
                    mac_address VARCHAR(17) NOT NULL,
                    description TEXT NOT NULL
                )
                """)
cursor.execute("""
                CREATE TABLE IF NOT EXISTS photos_taken(
                    photo_id NVARCHAR(36) PRIMARY KEY,
                    meter_id NVARCHAR(36) NOT NULL,
                    photo_path TEXT NOT NULL,
                    processed INTEGER DEFAULT 0,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (meter_id) REFERENCES meters(meter_id) ON DELETE CASCADE
                )
                """)
cursor.execute("""
                CREATE TABLE IF NOT EXISTS readings(
                    reading_id NVARCHAR(36) PRIMARY KEY,
                    photo_id NVARCHAR(36) NOT NULL,
                    read_value TEXT NOT NULL,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (photo_id) REFERENCES photos_taken(photo_id) ON DELETE CASCADE
                )
                """)

conn.commit()
conn.close()

print("Database initialized successfully")