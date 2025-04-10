import json
from kafka import KafkaConsumer
import psycopg2
from config.settings import DB_CONFIG
from gcs.downloader import download_pdf_from_gcs
from parser.pdf_text_extractor import extract_text_from_pdf
from parser.trace_cleaner import process_pdf_text, extract_metadata_from_filename
from db.db_insert import store_in_database
from embedding.chunker import chunk_document_data
from embedding.embedder import get_openai_embedding
from embedding.pinecone_uploader import upload_chunks_to_pinecone
from config.settings import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX
import os

consumer = KafkaConsumer(
    "gcs-topic",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="pdf-processing-group"
)

print("📥 Kafka Consumer is running and waiting for PDF upload events...")

conn = psycopg2.connect(**DB_CONFIG)

for message in consumer:
    data = message.value
    bucket = data["bucket"]
    file_name = data["file"]

    print(f"📂 Processing file: {file_name} from bucket: {bucket}")

    local_dir = "../pdfs"
    os.makedirs(local_dir, exist_ok=True)
    local_path = os.path.join(local_dir, os.path.basename(file_name))

    # Download, extract, parse, store
    download_pdf_from_gcs(bucket, file_name, local_path)
    text = extract_text_from_pdf(local_path)
    parsed_data = process_pdf_text(text)
    parsed_data["course_info"].update(extract_metadata_from_filename(file_name))
    document_id = store_in_database(conn, parsed_data, file_name)

    # Vectorize and send to Pinecone
    if document_id:
        print("🔗 Chunking document for embedding...")
        # Build chunks from just this document
        chunked_data = chunk_document_data({
            "document_id": document_id,
            "document_name": file_name,
            "full_text": parsed_data["full_text"],
            "comments": parsed_data.get("comments", []),
            "professor": parsed_data["course_info"].get("instructor", "Unknown")
        })

        upload_chunks_to_pinecone(
            chunked_data,
            index_name=PINECONE_INDEX,
            api_key=PINECONE_API_KEY,
            environment=PINECONE_ENVIRONMENT
        )

        print(f"✅ Vectorized and uploaded document ID {document_id} to Pinecone.")

    print(f"✅ Stored '{file_name}' to PostgreSQL.\n")
