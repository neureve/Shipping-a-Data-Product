from dagster import job
from assets.scrape import scrape_telegram_data
from assets.load import load_raw_to_postgres
from assets.transform import run_dbt_transformations
from assets.enrich import run_yolo_enrichment

@job
def full_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres()
    enrich = run_yolo_enrichment()
    transform = run_dbt_transformations()

    load.after(scrape)
    enrich.after(load)
    transform.after(enrich)
