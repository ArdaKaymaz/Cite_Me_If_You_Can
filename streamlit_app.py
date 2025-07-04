import streamlit as st
import requests
import json

# 🧠 Session state flags
if "chunks_uploaded" not in st.session_state:
    st.session_state["chunks_uploaded"] = False
if "search_done" not in st.session_state:
    st.session_state["search_done"] = False
if "answer_json_uploaded" not in st.session_state:
    st.session_state["answer_json_uploaded"] = False
if "answer_json_content" not in st.session_state:
    st.session_state["answer_json_content"] = None

# 📄 Title and Tabs
st.set_page_config(page_title="Cite Me If You Can", layout="wide")
st.title("📚 Cite Me If You Can")

tabs = st.tabs(["📥 Upload & Search", "🤖 LLM Answer"])

# ─────────────────────────────────────────────────────────────
# 🧩 TAB 1: Upload & Search
with tabs[0]:
    st.header("1. Upload Chunks")

    # Send JSON file to API right after it was uploaded
    uploaded_file = st.file_uploader("Upload a JSON file with chunks", type=["json"])

    if uploaded_file:
        try:
            file_content = uploaded_file.read().decode("utf-8")
            chunks = json.loads(file_content)

            # API'ye gönderim
            response = requests.put("http://localhost:8000/api/upload", json={"chunks": chunks})
            if response.status_code == 200:
                st.session_state["chunks_uploaded"] = True
                st.session_state["search_done"] = False
                st.success(f"✅ Upload successful. {response.json()['count']} chunks uploaded.")
            else:
                st.error(f"❌ Upload failed: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ Invalid JSON file: {e}")
            st.session_state["chunks_uploaded"] = False

    # ────────────────────────────────
    # 🔍 Similarity Search
    if st.session_state.get("chunks_uploaded", False):
        st.header("2. Similarity Search")

        with st.form("similarity_search_form"):
            query = st.text_input("Query", value="What are the benefits of growing mucuna?")
            k = st.number_input("Top K Results", min_value=1, max_value=20, value=5)
            min_score = st.slider("Minimum Score", 0.0, 1.0, 0.25, 0.01)
            submitted = st.form_submit_button("🔍 Run Similarity Search")

        if submitted:
            try:
                payload = {
                    "query": query,
                    "k": k,
                    "min_score": min_score
                }
                response = requests.post("http://localhost:8000/api/similarity_search", json=payload)
                if response.status_code == 200:
                    results = response.json()
                    st.session_state["search_done"] = True
                    st.success(f"✅ Found {len(results)} similar chunks.")
                    for i, item in enumerate(results, 1):
                        st.markdown(f"""
                        **{i}. Score:** `{item['score']:.3f}`  
                        **Section:** *{item['section_heading']}*  
                        **Source:** `{item['source_doc_id']}`  
                        > {item['text'][:500]}...
                        """)
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
    else:
        st.info("ℹ️ Please upload a valid chunk file before running similarity search.")

    # ────────────────────────────────
    # 📄 Get Chunks by Journal ID
    if st.session_state.get("chunks_uploaded", False):
        st.header("3. Get Chunks by Journal ID")

        with st.form("get_journal_form"):
            journal_id = st.text_input("Enter source_doc_id (e.g., extension_brief_mucuna.pdf)")
            get_chunks = st.form_submit_button("📄 Get Chunks")

        if get_chunks:
            try:
                response = requests.get(f"http://localhost:8000/api/{journal_id}")
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Found {data['chunk_count']} chunks.")
                    for i, chunk in enumerate(data["chunks"], 1):
                        st.markdown(f"""
                        **{i}. Section:** *{chunk['section_heading']}*  
                        > {chunk['text'][:500]}...
                        """)
                else:
                    st.error(f"❌ {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
    else:
        st.info("ℹ️ Please run a similarity search first.")

# ─────────────────────────────────────────────────────────────
# 🤖 TAB 2: LLM Answer
with tabs[1]:
    st.header("🤖 LLM Answer")

    # ⛔ Refresh previous data (LLM tab works isolated)
    st.session_state["chunks_uploaded"] = False
    st.session_state["search_done"] = False
    st.session_state["vector_data_llm"] = None
    st.session_state["llm_ready"] = False

    # 1. Dosya yükleme
    uploaded = st.file_uploader("Upload a JSON file with chunks (LLM mode)", type=["json"], key="llm_uploader")

    if uploaded:
        try:
            content = uploaded.read().decode("utf-8")
            data = json.loads(content)

            # API'ye gönder
            with st.spinner("Uploading chunks to LLM memory..."):
                response = requests.put("http://localhost:8000/api/upload", json={"chunks": data})
                if response.status_code == 200:
                    st.success("✅ Chunks uploaded successfully.")
                    st.session_state["llm_ready"] = True
                else:
                    st.error(f"❌ Upload failed: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ Invalid JSON: {e}")
            st.session_state["llm_ready"] = False

    # 2. If file was uploaded, query panel is active
    if st.session_state.get("llm_ready"):
        st.markdown("### 🔍 Ask your question")

        with st.form("llm_query_form"):
            query = st.text_input("Enter your question", value="What are the benefits of growing mucuna?")
            k = st.number_input("Top K Chunks", min_value=1, max_value=20, value=5, step=1)
            min_score = st.slider("Minimum Similarity Score", 0.0, 1.0, 0.25, step=0.01)
            submitted = st.form_submit_button("🧠 Generate LLM Answer")

        if submitted:
            try:
                payload = {
                    "query": query,
                    "k": k,
                    "min_score": min_score
                }
                response = requests.post("http://localhost:8000/api/answer", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.markdown("### ✅ Answer")
                    st.markdown(result["answer"])

                    st.markdown("### 📚 Source Chunks")
                    for i, chunk in enumerate(result["sources"], 1):
                        st.markdown(f"""
                        **{i}. Section:** *{chunk['section_heading']}*  
                        **Score:** `{chunk['score']:.3f}`  
                        **Text:**  
                        > {chunk['text'][:500]}...
                        """)
                else:
                    st.error(f"❌ API error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
    else:
        st.info("ℹ️ Please upload a JSON file to enable LLM query interface.")
