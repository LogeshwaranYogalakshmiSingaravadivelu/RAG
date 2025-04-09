from google.cloud import storage
from google.oauth2 import service_account
from config.settings import GCP_KEY_PATH

def download_pdf_from_gcs(bucket_name, file_name, local_path):
    credentials = service_account.Credentials.from_service_account_file(GCP_KEY_PATH)
    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(local_path)
    print(f"Downloaded {file_name} to {local_path}")
