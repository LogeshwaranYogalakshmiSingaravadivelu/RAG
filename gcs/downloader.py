import os
from google.cloud import storage
from google.oauth2 import service_account

def download_pdf_from_gcs(bucket_name, file_name, local_path):
    gcp_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    credentials = service_account.Credentials.from_service_account_file(gcp_key_path)
    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(local_path)
    print(f"✅ Downloaded {file_name} to {local_path}")
