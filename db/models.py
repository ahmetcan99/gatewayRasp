from . import DB_PATH
from typing import List, Tuple
import sqlite3
import uuid
import os

def add_new_meter(meter_uuid, meter_mac, meter_description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO meters (meter_id, mac_address, description) 
                   Values(?, ?, ?)
    """, (meter_uuid, meter_mac, meter_description,))
    conn.commit()
    conn.close()
    print(f"New meter {meter_mac}, added with {meter_uuid} uuid to database.")

def get_meter_uuid_with_mac(meter_mac):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT meter_id FROM meters WHERE mac_address = ?
    """,(meter_mac,))
    result = cursor.fetchone()
    
    conn.close()
    if result:
        return str(result[0])
    else:
        return None

def get_all_meters() -> List[Tuple[str,str]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meters")
    meters = cursor.fetchall()
    conn.close()
    return meters

def add_photo(image_uuid: str, meter_id: str, photo_path: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO photos_taken (photo_id, meter_id, photo_path) VALUES (?, ?, ?)", (image_uuid,meter_id, photo_path))
        conn.commit()
        print(f"Photo added: {image_uuid}, for meter {meter_id}")
    except sqlite3.IntegrityError:
        print(f"Photo couldn't added: {image_uuid}, for meter {meter_id}")
    finally:
        conn.close()

def get_photos_by_meter(meter_id: str) -> List[Tuple[int, str, str]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM photos_taken WHERE meter_id = ?", (meter_id,))
    photos = cursor.fetchall()
    conn.close()
    return photos

def get_last_photo_by_meter(photo_id: str) -> Tuple[int, str, str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM photos_taken WHERE photo_id = ?
                   ORDER BY date DESC
                   LIMIT 1
                   """,(photo_id,))
    photo = cursor.fetchone()
    conn.close()
    return photo

def get_reading(photo_id: str) -> Tuple[int, str, float]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM readings WHERE photo_id = ?", (photo_id,))
    reading = cursor.fetchone()
    
    conn.close()
    return reading

def add_reading(photo_id: str, reading_value: str):
    reading_uuid = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO readings (reading_id, photo_id, read_value) VALUES (?, ?, ?)", (reading_uuid, photo_id, reading_value))
        cursor.execute("UPDATE photos_taken SET processed = 1 WHERE photo_id = ?", (photo_id,))
        conn.commit()
        print(f"Reading added for photo {photo_id}: {reading_value}")
    except sqlite3.IntegrityError:
        print(f"Reading couldn't be added: {photo_id} already exists.")
    finally:
        conn.close()