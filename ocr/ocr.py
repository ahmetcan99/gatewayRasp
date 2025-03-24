import cv2
import pytesseract
import sqlite3
import time
import numpy as np
from typing import List, Tuple
from db import DB_PATH
from db import models

INTERVAL = 40

def get_unprocessed_images() -> List[Tuple[str, str]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT photo_id, photo_path 
        FROM photos_taken 
        WHERE processed = 0 
        ORDER BY date ASC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return rows 

def process_image(image_path: str) -> str:
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Hough Lines kullanarak çizgileri bul
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    angles = []
    if lines is not None:
        for rho, theta in lines[:, 0]:
            angle = (theta * 180 / np.pi) - 90  # Açı hesapla
            angles.append(angle)

    # Medyan açıyı bul ve döndür
    median_angle = np.median(angles) if angles else 0

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    data_normal = pytesseract.image_to_data(rotated, lang="tur", output_type=pytesseract.Output.DICT)

    extracted_text = ""

    for i in range(len(data_normal["text"])):
        if int(data_normal["conf"][i]) > 50: 
            text = data_normal["text"][i].strip()
            if text:
                extracted_text += text + " "
    
    return extracted_text

def process_unprocessed_images():
    images = get_unprocessed_images()
    
    if not images:
        print("No unprocessed images found.")
        return
    
    for photo_id, image_path in images:
        print(f"Processing: {image_path}")
        reading_text = process_image(image_path)
        models.add_reading(photo_id, reading_text)
        print(f"Processed {photo_id}, saved reading.")

def run(interval: int = INTERVAL):
    while True:
        process_unprocessed_images()
        print(f"Sleeping for {interval} seconds...")
        time.sleep(interval)

if __name__ == "__main__":
    run()