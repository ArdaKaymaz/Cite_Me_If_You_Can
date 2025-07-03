import streamlit as st
import requests
import json

# Header
st.set_page_config(page_title="Cite Me If You Can", layout="wide")
st.title("📚 Cite Me If You Can — Semantic Search & Summarizer")

# Session state: Was the upload completed?
if "chunks_uploaded" not in st.session_state:
    st.session_state["chunks_uploaded"] = False

# 1️⃣ Upload Chunks
st.header("1. Upload Chunks (Sample_chunks.json)")
uploaded_file = st.file_uploader("Upload a JSON file with chunks", type=["json"])

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
                st.session_state["chunks_uploaded"] = True
                st.success(f"✅ Upload successful. {response.json()['count']} chunks uploaded.")
            else:
                st.error(f"❌ Upload failed: {response.text}")
    except Exception as e:
        st.error(f"❌ Invalid JSON file: {str(e)}")

# 2️⃣ Similarity Search (Show if only the upload was completed)
if st.session_state["chunks_uploaded"]:
    st.header("2. Similarity Search")

    with st.form("similarity_search_form"):
        query = st.text_input("Query", value="What are the benefits of growing mucuna?")
        k = st.number_input("Top K Results", min_value=1, max_value=20, value=5, step=1)
        min_score = st.slider("Minimum Score", min_value=0.0, max_value=1.0, value=0.25, step=0.01)
        submitted = st.form_submit_button("🔍 Run Similarity Search")

    if submitted:
        payload = {
            "query": query,
            "k": k,
            "min_score": min_score
        }

        try:
            response = requests.post("http://localhost:8000/api/similarity_search", json=payload)
            if response.status_code == 200:
                results = response.json()
                st.success(f"✅ Found {len(results)} similar chunks.")
                for i, item in enumerate(results, 1):
                    st.markdown(f"""
                    **{i}. Score:** `{item['score']:.3f}`  
                    **Section:** *{item['section_heading']}*  
                    **Source:** `{item['source_doc_id']}`  
                    **Text:**  
                    > {item['text'][:500]}...
                    """)
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
else:
    st.info("ℹ️ Please upload a JSON chunk file before running similarity search.")