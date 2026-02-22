import os
import re
import uuid
import chromadb
from sentence_transformers import SentenceTransformer
from services.pdf_parser import extract_text_from_pdf

# Local embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma persistent client
chroma_client = chromadb.PersistentClient(
    path="knowledge_base/chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="medical_guidelines"
)
def get_embedding(text: str):
    embedding = embedding_model.encode(text)
    return embedding.tolist()





# SMART CHUNKING FUNCTION


def smart_chunk_text(text: str,
                     min_chunk_size=300,
                     max_chunk_size=900,
                     overlap=150):

    # -------------------------
    # 1️⃣ Clean text
    # -------------------------
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text).strip()

    # -------------------------
    # 2️⃣ Try semantic heading split
    # -------------------------
    heading_pattern = r'(?=\b[A-Z][A-Z\s]{4,}\b)'  # ALL CAPS headings
    sections = re.split(heading_pattern, text)

    semantic_chunks = []

    for section in sections:
        section = section.strip()
        if len(section) >= min_chunk_size:
            semantic_chunks.append(section)

    # -------------------------
    # 3️⃣ If semantic split works (>=3 chunks) → refine by size
    # -------------------------
    if len(semantic_chunks) >= 3:

        final_chunks = []

        for section in semantic_chunks:
            if len(section) <= max_chunk_size:
                final_chunks.append(section)
            else:
                # Split oversized section using window method
                start = 0
                while start < len(section):
                    end = start + max_chunk_size
                    chunk = section[start:end]
                    if len(chunk) >= min_chunk_size:
                        final_chunks.append(chunk)
                    start += max_chunk_size - overlap

        return final_chunks

    # -------------------------
    # 4️⃣ Fallback: Pure window chunking
    # -------------------------
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chunk_size
        chunk = text[start:end]
        if len(chunk) >= min_chunk_size:
            chunks.append(chunk)
        start += max_chunk_size - overlap

    return chunks

def ingest_pdf_to_kb(pdf_path: str):

    print(f"Processing: {pdf_path}")

    text = extract_text_from_pdf(pdf_path)

    chunks = smart_chunk_text(text)

    for chunk in chunks:
        embedding = get_embedding(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(uuid.uuid4())],
            metadatas=[{"source": os.path.basename(pdf_path)}]
        )

    print(f"Ingested {len(chunks)} chunks successfully!")
    
if __name__ == "__main__":
    
    pdf_folder = "knowledge_base/raw_docs"

    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            full_path = os.path.join(pdf_folder, file)
            ingest_pdf_to_kb(full_path)

    print("Knowledge Base Build Complete.")