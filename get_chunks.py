import json
import requests

# 1. Input the journal id you asked for
journal_id = "extension_brief_mucuna.pdf"

# 2. Send GET request to API
url = f"http://localhost:8000/api/{journal_id}"
response = requests.get(url)

# 3. Check the response and print in format
if response.status_code == 200:
    formatted = json.dumps(response.json(), indent=4, ensure_ascii=False)
    print(formatted)
else:
    print(f"❌ Error {response.status_code}: {response.text}")