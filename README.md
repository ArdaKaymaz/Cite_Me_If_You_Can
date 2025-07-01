# Cite Me If You Can
 Will AI replace scientists?
 Maybe will, maybe won't, but I'm sure it is helpful for scientists.

## 📚 System Architecture and Design Decisions

This section outlines the key components of the ingestion and retrieval pipeline used in the *Cite Me If You Can* project. Each part of the system is carefully selected and designed to ensure high-quality, citation-aware scientific document processing.

---

### 1️⃣ Scheduled Daily New File Detection and Duplicate Filtering

**Purpose**: Systematically identify and ingest only truly new journal files while filtering out near-duplicates to maintain a clean, efficient vector store.

#### 🔁 Process Flow
- **Scheduled Execution**:  
  A daily cronjob (or equivalent scheduler) automatically triggers a script to scan the secure upload directory for new files.  
  _**Why:** Ensures hands-free, consistent ingestion._

- **New File Detection**:  
  Compares current files against previously processed records to find newly added documents.  
  _**Why:** Prevents redundant processing of existing documents._

- **Duplicate Detection via Cosine Similarity**:  
  Embeddings of new documents are compared with previously ingested ones using cosine similarity.  
  _**Why:** Captures semantic duplicates even if text is slightly altered._

- **Duplicate Filtering Threshold**:  
  Files with >**99%** cosine similarity are excluded from further processing.  
  _**Why:** Avoids cluttering the vector store with near-identical content._

- **Pipeline Continuation**:  
  Only sufficiently unique files proceed to chunking, embedding, and indexing.  
  _**Why:** Preserves relevance and diversity in the database._

---

### 2️⃣ Chunking Strategy for Scientific Articles

**Purpose**: Enable accurate retrieval and better embedding by maintaining logical and semantic coherence in the content chunks.

#### 🧠 Strategy
- **Section-Based Segmentation**:  
  Articles are first split into major sections (e.g., Abstract, Introduction, Methods).  
  _**Why:** Scientific papers follow a well-defined structure, and each section represents a unique conceptual unit._

- **Paragraph-Level Chunking**:  
  Within each section, content is divided into individual paragraphs.  
  _**Why:** Academic paragraphs typically express a single idea or finding — making them ideal minimal retrieval units._

#### ✅ Benefits
- Preserves academic structure and intent
- Boosts embedding relevance
- Improves semantic search and generative grounding

---

### 3️⃣ Embedding Strategy – Using SPECTER2

**Purpose**: Represent each content chunk as a dense vector that captures scientific meaning and citation context.

#### 🤖 Model: `SPECTER2` (by AllenAI)
- **Why SPECTER2?**
  - Specifically trained on scientific literature
  - Incorporates **citation relationships** into embeddings
  - Outperforms general-purpose models in tasks like:
    - Scientific paper retrieval
    - Semantic similarity search
    - Citation prediction

#### 📈 Result
By embedding each chunk with SPECTER2, the system builds a semantically rich, citation-aware knowledge base, enhancing both the **retrieval accuracy** and the **trustworthiness** of LLM-generated outputs. 