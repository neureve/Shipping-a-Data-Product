# scraping/run_scraper.py

from scraping.telegram_scraper import scrape_channel

channels = [
    "lobelia4cosmetics",
    "tikvahpharma",
    "ChemedChannelUsername"  # Replace with correct one
]

for ch in channels:
    scrape_channel(ch)
