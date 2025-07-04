# 🧠 Cite Me If You Can - Semantic Search & LLM Summarization

## 🧩 Vector Database & LLM Integration
This project uses a **mock in-memory vector store** (a simple Python list) to simulate a vector database. Although the final implementation will leverage a more robust system like **Weaviate**, this prototype focuses on functionality and rapid development. If more time were available, the system would be containerized using **Docker** and connected to a **real vector database** for persistent storage and advanced querying.

## 🎨 Frontend UI
The frontend is built using **Streamlit**, chosen for its simplicity, speed, and prior developer experience. It enables a fully interactive web interface with clear separation between functional areas:

- 📤 **Upload & Search tab**: Upload chunked JSON data, perform similarity search, and retrieve journal chunks.
- 🤖 **LLM Answer tab**: Generate an answer using an LLM from semantically relevant chunks.

Each section is controlled using `st.session_state` to enforce clean state separation and prevent invalid actions (e.g., attempting search without uploading data).

## 🧠 Content-Generation with Gemini 2.5 Flash
The app integrates with **Google's Gemini 2.5 Flash model** via the `google.generativeai` API. It performs the following pipeline:

1. Accepts a natural-language question.
2. Performs a semantic similarity search over the uploaded chunk vectors (using **SPECTER2 embeddings**).
3. Sends the most relevant chunks to Gemini with a concise, instruction-tuned prompt.
4. Returns a professional, cited scientific summary.

## 📚 Auto-generated References
After generating the LLM response, the app automatically generates citations in the three most widely used formats:

- **📘 APA Style**
- **📗 MLA Style**
- **📙 Chicago Style**

All three formats are displayed immediately following the answer, formatted using code blocks (`st.code`) for easy copy-paste.

---

## ✅ Example Workflow
1. Upload a `Sample_chunks.json` file.
2. Enter a natural query like `"What are the benefits of growing mucuna?"`
3. Submit for semantic search or directly query the LLM.
4. View the concise answer and relevant references instantly.

