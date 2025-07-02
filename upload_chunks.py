import json
import requests

# Read raw chunks
with open("Sample_chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Convert each chunk into expected format
formatted_chunks = []
for chunk in chunks_data:
    formatted_chunks.append({
        "text": chunk["text"],
        "source_doc_id": chunk["source_doc_id"],
        "section_heading": chunk["section_heading"],
        "journal": chunk["journal"],
        "publish_year": chunk["publish_year"],
        "attributes": {f"attr_{i}": attr for i, attr in enumerate(chunk.get("attributes", []))}
    })

# Final payload
payload = {"chunks": formatted_chunks}

# API endpoint
API_URL = "http://127.0.0.1:8000/api/upload"

# Send to API
response = requests.put(API_URL, json=payload)

# Print result
print("Status code:", response.status_code)
print("Response:", response.json())