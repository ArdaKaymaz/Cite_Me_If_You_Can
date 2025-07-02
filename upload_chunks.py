import json
import requests

# Read JSON file
with open("Sample_chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Convert into API suitable format
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

payload = {"chunks": formatted_chunks}

# API address
API_URL = "http://127.0.0.1:8000/api/upload"

# Send request
response = requests.put(API_URL, json=payload)

print("Status code:", response.status_code)
print("Response:", response.json())