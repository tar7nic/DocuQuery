from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

def get_client():
    client = QdrantClient(url=QDRANT_URL,api_key=QDRANT_API_KEY)
    return client

def create_collection(client):
    existing = [c.name for c in client.get_collections().collections]
    if "research_docs" not in existing:  # only create if it doesn't exist
        client.create_collection(
            collection_name="research_docs",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        
def upsert_chunks(client, chunks, vectors):
    batch_size = 100
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=vector, payload=chunk)
        for chunk, vector in zip(chunks, vectors)
    ]
    
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name="research_docs",
            wait=True,
            points=batch
        )
        print(f"Upserted batch {i//batch_size + 1}")
    
def search(client, query_vector, top_k=10):
    results = client.query_points(
        collection_name="research_docs",
        query = query_vector, 
        limit = top_k
    ).points
    return results

if __name__ == "__main__":
    client = get_client()
    create_collection(client)
    print("Connected and collection created!")