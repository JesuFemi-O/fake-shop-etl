import os
import csv
import io
import random
import uuid
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

def generate_customer_orders():
    num_orders = random.randint(5, 30)
    orders = []

    for order_id in range(1, num_orders + 1):
        customer_id = random.randint(1000, 9999)
        product_id = random.randint(1, 100)
        quantity = random.randint(1, 10)
        total_amount = round(random.uniform(10, 100), 2)

        order = [order_id, customer_id, product_id, quantity, total_amount]
        orders.append(order)

    return orders

def upload_to_gcs(bucket_name, file_name, data, environment):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    unique_id = str(uuid.uuid4())[:8]  # Generate a random 8-character UUID
    # 
    full_file_name = f"{environment.lower()}/{file_name}_{unique_id}.csv"

    # Convert list of lists to CSV string
    csv_string = io.StringIO()
    csv_writer = csv.writer(csv_string)
    csv_writer.writerow(['OrderID', 'CustomerID', 'ProductID', 'Quantity', 'TotalAmount'])
    csv_writer.writerows(data)

    # Upload the CSV string to GCS
    blob = bucket.blob(full_file_name)
    blob.upload_from_string(csv_string.getvalue(), content_type='text/csv')

    print(f"successfully uploaded file {full_file_name}")

if __name__ == "__main__":
    environment = os.environ.get('ENVIRONMENT', 'PROD')
    file_name = 'customer_orders'

    bucket_name = 'fake-shop-lake-v2'
    orders = generate_customer_orders()
    upload_to_gcs(bucket_name, file_name, orders, environment)
