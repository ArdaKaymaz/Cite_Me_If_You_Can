import json
import requests

# 1. Read query.json
with open("query.json", "r", encoding="utf-8") as f:
    payload = json.load(f)

# 2. Send POST request to API
response = requests.post(
    "http://localhost:8000/api/similarity_search",
    json=payload,
    headers={"Content-Type": "application/json"}
)

# 3. Check the response and print in format
if response.status_code == 200:
    formatted = json.dumps(response.json(), indent=4, ensure_ascii=False)
    print(formatted)
else:
    print(f"❌ Error {response.status_code}: {response.text}")