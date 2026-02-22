import chromadb
from sentence_transformers import SentenceTransformer

# Load same embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to existing Chroma DB
chroma_client = chromadb.PersistentClient(
    path="knowledge_base/chroma_db"
)

collection = chroma_client.get_collection(
    name="medical_guidelines"
)


def get_embedding(text: str):
    return embedding_model.encode(text).tolist()


def retrieve_relevant_chunks(query_text: str, top_k: int = 2):

    query_embedding = get_embedding(query_text)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "distances"]
    )

    print("\nDistances:", results["distances"][0])  

    return results["documents"][0]