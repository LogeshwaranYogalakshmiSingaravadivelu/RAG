import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'dbname': 'yourdbname',
    'user': 'youruser',
    'password': 'yourpassword',
    'host': 'postgres',
    'port': 5432
}

BUCKET_NAME = 'csye7125-trace-documents'
LOCAL_PDF_DIR = 'pdfs'
GCP_KEY_PATH = os.getenv("GCP_KEY_PATH")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
