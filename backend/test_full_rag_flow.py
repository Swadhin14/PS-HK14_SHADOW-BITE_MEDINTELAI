from services.query_builder import build_query_from_structured_data
from services.rag_retriever import retrieve_relevant_chunks

# Simulated structured output (like your extractor gives)
structured_data = [
    {
        "test_name": "Fasting Blood Sugar",
        "value": "105",
        "unit": "mg/dL",
        "normal_range": "70 - 100",
        "status": "Slightly High"
    },
    {
        "test_name": "Vitamin D",
        "value": "18",
        "unit": "ng/mL",
        "normal_range": "20 - 50",
        "status": "Low"
    }
]

query = build_query_from_structured_data(structured_data)

print("\nGenerated Query:\n")
print(query)

results = retrieve_relevant_chunks(query)

print("\nRetrieved WHO Chunks:\n")

for i, chunk in enumerate(results, 1):
    print(f"\n--- Chunk {i} ---\n")
    print(chunk[:500])