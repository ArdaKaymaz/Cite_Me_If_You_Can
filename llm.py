import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def summarize_chunks(query: str, chunks: list[str]) -> str:
    prompt = f"""
You are a concise and professional science writer for a popular science magazine.

[BEGIN]
User Query: {query}

Relevant Chunks:
{chr(10).join(f"- {chunk}" for chunk in chunks)}
[END]

Please provide a concise summary based on the above information.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[LLM Error] {str(e)}"