from embedding.pinecone_uploader import upload_chunks_to_pinecone
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")

if __name__ == "__main__":
    upload_chunks_to_pinecone(PINECONE_INDEX_NAME, PINECONE_API_KEY, PINECONE_ENVIRONMENT)
