# enrichment/detect_objects.py

import os
import json
from ultralytics import YOLO
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import psycopg2

# Load env vars
load_dotenv()

# DB connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)
cur = conn.cursor()

# Load YOLO model
model = YOLO("yolov8n.pt")

# Folder to scan
images_root = Path("data/raw/images")

# Loop through all images
for date_dir in images_root.iterdir():
    for channel_dir in date_dir.iterdir():
        for img_file in channel_dir.glob("*.jpg"):
            logger.info(f"🔍 Processing {img_file}")
            results = model(str(img_file))

            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    confidence = float(box.conf[0])

                    # Parse message ID from image filename
                    msg_id = int(img_file.stem)

                    # Insert detection to PostgreSQL
                    try:
                        cur.execute("""
                            INSERT INTO raw_image_detections (message_id, detected_object_class, confidence_score)
                            VALUES (%s, %s, %s)
                            ON CONFLICT DO NOTHING;
                        """, (msg_id, class_name, confidence))
                    except Exception as e:
                        logger.warning(f"Failed to insert: {e}")

conn.commit()
cur.close()
conn.close()
# YOLOv8 Image Detection Script
