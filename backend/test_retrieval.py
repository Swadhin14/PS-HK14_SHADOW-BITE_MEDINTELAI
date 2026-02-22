from services.rag_retriever import retrieve_relevant_chunks

query = "diagnosis criteria for diabetes and high blood glucose"

results = retrieve_relevant_chunks(query)

print("\nTop Retrieved Chunks:\n")

for i, chunk in enumerate(results, 1):
    print(f"\n--- Chunk {i} ---\n")
    print(chunk[:500])