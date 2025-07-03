import streamlit as st
import requests
import json

st.title("📚 Cite Me If You Can — Semantic Search & Summarizer")

st.header("1. Upload Chunks (Sample_chunks.json)")
uploaded_file = st.file_uploader("Upload JSON file with chunks", type=["json"])

if uploaded_file:
    try:
        file_content = uploaded_file.read().decode("utf-8")
        data = json.loads(file_content)

        if st.button("📤 Upload Chunks to API"):
            response = requests.put(
                "http://localhost:8000/api/upload",
                json={"chunks": data}
            )
            if response.status_code == 200:
                st.success(f"✅ Upload successful. {response.json()['count']} chunks uploaded.")
            else:
                st.error(f"❌ Upload failed: {response.text}")
    except Exception as e:
        st.error(f"❌ Invalid JSON file: {str(e)}")