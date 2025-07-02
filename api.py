from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uuid
import numpy as np
from embedding import embed_text  # SPECTER2 function from embedding.py

app = FastAPI()

# Temporary vector db
vector_store = []

# Data models
class Chunk(BaseModel):
    text: str
    source_doc_id: str
    section_heading: str
    journal: str
    publish_year: int
    attributes: Optional[Dict[str, str]] = Field(default_factory=dict)

class UploadRequest(BaseModel):
    chunks: List[Chunk]

class SimilaritySearchRequest(BaseModel):
    query: str
    k: int = 10
    min_score: float = 0.25

class SearchResult(BaseModel):
    id: str
    text: str
    score: float
    source_doc_id: str
    section_heading: str
    journal: str
    publish_year: int
    attributes: Optional[Dict[str, str]]


# Upload endpoint
@app.put("/api/upload")
def upload_chunks(payload: UploadRequest):
    for chunk in payload.chunks:
        embedding = embed_text(chunk.text)
        vector_store.append({
            "id": str(uuid.uuid4()),
            "text": chunk.text,
            "embedding": embedding,
            "source_doc_id": chunk.source_doc_id,
            "section_heading": chunk.section_heading,
            "journal": chunk.journal,
            "publish_year": chunk.publish_year,
            "usage_count": 0,
            "attributes": chunk.attributes
        })
    return {
        "message": "Chunks uploaded successfully",
        "count": len(payload.chunks),
        "status": "accepted"
    }


# Cosine similarity calculator
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))

# Similarity search endpoint
@app.post("/api/similarity_search", response_model=List[SearchResult])
def similarity_search(request: SimilaritySearchRequest):
    if not vector_store:
        raise HTTPException(status_code=400, detail="Vector store is empty. Upload chunks first.")

    query_embedding = embed_text(request.query)

    scored_results = []
    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        if score >= request.min_score:
            scored_results.append({**item, "score": score})

    top_k = sorted(scored_results, key=lambda x: x["score"], reverse=True)[:request.k]

    return [
        SearchResult(
            id=item["id"],
            text=item["text"],
            score=item["score"],
            source_doc_id=item["source_doc_id"],
            section_heading=item["section_heading"],
            journal=item["journal"],
            publish_year=item["publish_year"],
            attributes=item.get("attributes", {})
        )
        for item in top_k
    ]