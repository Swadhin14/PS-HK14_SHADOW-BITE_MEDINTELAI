import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to existing ChromaDB
chroma_client = chromadb.PersistentClient(path="knowledge_base/chroma_db")
collection = chroma_client.get_collection("medical_guidelines")


def retrieve_from_kb(structured_data, top_k=5):

    # Convert structured labs into search query
    query_text = ""

    for lab in structured_data:
        if lab.get("status") != "Normal":
            query_text += f"{lab['test_name']} {lab['value']} {lab['unit']} {lab['status']}. "

    if not query_text:
        return []

    # Create embedding
    query_embedding = model.encode(query_text).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]