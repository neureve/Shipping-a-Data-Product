# scraping/telegram_scraper.py

import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from loguru import logger

# Load secrets
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")

# Setup logging
log_path = Path("logs/scraping.log")
log_path.parent.mkdir(parents=True, exist_ok=True)
logger.add(log_path, rotation="500 KB")

# Function to scrape a single channel
def scrape_channel(channel_username, limit=100):
    with TelegramClient(session_name, api_id, api_hash) as client:
        logger.info(f"Scraping: {channel_username}")
        messages = []
        for message in client.iter_messages(channel_username, limit=limit):
            messages.append(message.to_dict())

        # Save data
        today = datetime.now().strftime("%Y-%m-%d")
        out_dir = Path(f"data/raw/telegram_messages/{today}")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{channel_username.replace('@', '')}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        logger.success(f"Saved {len(messages)} messages from {channel_username} to {out_file}")
