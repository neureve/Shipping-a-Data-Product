from dagster import op

@op
def scrape_telegram_data():
    import scraping.run_scraper  # your existing scraper
