import os
import psycopg2
from google.cloud import storage
from google.oauth2 import service_account
from config.settings import DB_CONFIG, BUCKET_NAME, LOCAL_PDF_DIR, GCP_KEY_PATH
from gcs.downloader import download_pdf_from_gcs
from parser.pdf_text_extractor import extract_text_from_pdf
from parser.trace_cleaner import process_pdf_text, extract_metadata_from_filename
from db.db_init import initialize_database
from db.db_insert import store_in_database

def process_pdfs_in_bucket():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        initialize_database(conn)

        credentials = service_account.Credentials.from_service_account_file(GCP_KEY_PATH)
        client = storage.Client(credentials=credentials)
        bucket = client.get_bucket(BUCKET_NAME)

        for blob in bucket.list_blobs():
            if blob.name.endswith('.pdf'):
                local_path = os.path.join(LOCAL_PDF_DIR, blob.name)
                download_pdf_from_gcs(BUCKET_NAME, blob.name, local_path)

                pdf_text = extract_text_from_pdf(local_path)
                processed_data = process_pdf_text(pdf_text)

                metadata = extract_metadata_from_filename(blob.name)
                processed_data['course_info'].update(metadata)

                store_in_database(conn, processed_data, blob.name)

    finally:
        conn.close()

if __name__ == "__main__":
    os.makedirs(LOCAL_PDF_DIR, exist_ok=True)
    process_pdfs_in_bucket()
