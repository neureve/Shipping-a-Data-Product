# db/create_tables.py

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS raw_telegram_messages (
        id BIGINT PRIMARY KEY,
        date TIMESTAMP,
        sender_id BIGINT,
        message TEXT,
        channel TEXT,
        raw_json JSONB
    );
""")

conn.commit()
cur.close()
conn.close()

print("✅ Table created")

