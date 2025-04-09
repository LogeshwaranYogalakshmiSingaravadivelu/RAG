from pinecone import Pinecone, ServerlessSpec
from config.settings import DB_CONFIG
from embedding.chunker import generate_chunks_from_db
from embedding.embedder import get_openai_embedding


def upload_chunks_to_pinecone(index_name, api_key, environment):
    # Init Pinecone client
    pc = Pinecone(api_key=api_key)

    # Make sure index exists
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=environment.split("-")[0]  # extract region, e.g., "us-east-1"
            )
        )
        print(f"Created Pinecone index: {index_name}")

    index = pc.Index(index_name)

    # Generate and upload embeddings
    chunks = generate_chunks_from_db()
    for chunk in chunks:
        try:
            vector = get_openai_embedding(chunk["text"])
            index.upsert(vectors=[
                {
                    "id": chunk["id"],
                    "values": vector,
                    "metadata": {
                        "chunk_type": chunk["chunk_type"],
                        "text": chunk["text"]
                    }
                }
            ])
            print(f"✅ Uploaded: {chunk['id']}")
        except Exception as e:
            print(f"❌ Failed to upload {chunk['id']}: {e}")