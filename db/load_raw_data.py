# db/load_raw_data.py

import os
import json
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)

cur = conn.cursor()

def load_json_to_postgres(json_path, channel_name):
    with open(json_path, "r", encoding="utf-8") as f:
        messages = json.load(f)

    for msg in messages:
        try:
            cur.execute("""
                INSERT INTO raw_telegram_messages (id, date, sender_id, message, channel, raw_json)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                msg.get("id"),
                msg.get("date"),
                msg.get("sender_id"),
                msg.get("message"),
                channel_name,
                json.dumps(msg)
            ))
        except Exception as e:
            print(f"⚠️ Failed to insert message {msg.get('id')}: {e}")

    conn.commit()

# Load all files
base_dir = Path("data/raw/telegram_messages")
for date_dir in base_dir.iterdir():
    for file in date_dir.glob("*.json"):
        channel = file.stem
        print(f"📤 Loading {file}")
        load_json_to_postgres(file, channel)

cur.close()
conn.close()

print("✅ All data loaded to PostgreSQL")

