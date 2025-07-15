from dagster import op

@op
def run_yolo_enrichment():
    import enrichment.detect_objects
