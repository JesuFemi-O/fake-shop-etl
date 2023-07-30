import os
from google.cloud import bigquery
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

def process_file(event, context):
    bucket_name = event['bucket']
    file_name = event['name']

    print(f"Processing file: {file_name}")

    # Ignore files in the processed subfolder
    if file_name.startswith('dev/processed/') or file_name.startswith('prod/processed/'):
        return

    # Determine the environment based on the file prefix
    if file_name.startswith('dev/'):
        environment = 'DEV'
    elif file_name.startswith('prod/'):
        environment = 'PROD'
    else:
        # Invalid file prefix, log an error or handle appropriately
        return

    # Load CSV file into BigQuery
    bigquery_client = bigquery.Client()
    dataset_id = 'fake_shop'
    if environment == 'DEV':
        dataset_id = f'dev_{dataset_id}'  # Prefix dataset_id with "dev_"
    table_id = 'customer_orders'
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
    )

    uri = f"gs://{bucket_name}/{file_name}"
    load_job = bigquery_client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()

    if environment == 'PROD':
        # Move the file to the processed subfolder
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        source_blob = bucket.blob(file_name)
        
        new_file_name = f"{environment.lower()}/processed/{file_name.split('/')[-1]}"
        destination_blob = bucket.blob(new_file_name)
        destination_blob.rewrite(source_blob)
        source_blob.delete()

if __name__ == "__main__":
    # This is for local testing, but the function will be triggered by GCS events in the cloud
    event_data = {
        "bucket": "fake-shop-lake",
        "name": "dev/customer_orders.csv"
    }
    process_file(event_data, None)
