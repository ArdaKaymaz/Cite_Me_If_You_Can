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