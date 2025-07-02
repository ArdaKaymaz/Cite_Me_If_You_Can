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