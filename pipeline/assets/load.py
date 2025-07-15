from dagster import op

@op
def load_raw_to_postgres():
    import db.load_raw_data
