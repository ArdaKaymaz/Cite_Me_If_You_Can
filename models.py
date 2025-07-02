from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Chunk(BaseModel):
    text: str
    source_doc_id: str
    section_heading: str
    journal: str
    publish_year: int
    attributes: Dict[str, str] = Field(default_factory=dict)

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
    attributes: Dict[str, str]

class AnswerRequest(BaseModel):
    query: str
    k: int = 5
    min_score: float = 0.25

class AnswerResponse(BaseModel):
    answer: str
    sources: List[SearchResult]