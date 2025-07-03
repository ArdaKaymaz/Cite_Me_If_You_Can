from fastapi import FastAPI, HTTPException
from uuid import uuid4
from typing import List

from embedding import embed_text
from llm import summarize_chunks
from models import (
    Chunk,
    UploadRequest,
    SimilaritySearchRequest,
    SearchResult,
    AnswerRequest,
    AnswerResponse
)
from vector_utils import vector_store, cosine_similarity

app = FastAPI()

# Upload endpoint
@app.put("/api/upload")
def upload_chunks(payload: UploadRequest):
    for chunk in payload.chunks:
        embedding = embed_text(chunk.text)
        vector_store.append({
            "id": str(uuid4()),
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

# Similarity search
@app.post("/api/similarity_search", response_model=List[SearchResult])
def similarity_search(request: SimilaritySearchRequest):
    if not vector_store:
        raise HTTPException(status_code=400, detail="Vector store is empty. Upload chunks first.")

    query_embedding = embed_text(request.query)
    scored_chunks = []

    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        if score >= request.min_score:
            scored_chunks.append({**item, "score": score})

    top_k = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)[:request.k]

    return [
        SearchResult(
            id=chunk["id"],
            text=chunk["text"],
            score=chunk["score"],
            source_doc_id=chunk["source_doc_id"],
            section_heading=chunk["section_heading"],
            journal=chunk["journal"],
            publish_year=chunk["publish_year"],
            attributes=chunk.get("attributes", {})
        ) for chunk in top_k
    ]

# GET chunks by source_doc_id
@app.get("/api/{journal_id}")
def get_journal_chunks(journal_id: str):
    matching = [c for c in vector_store if c["source_doc_id"] == journal_id]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No chunks found for journal_id: {journal_id}")
    
    return {
        "source_doc_id": journal_id,
        "chunk_count": len(matching),
        "chunks": [
            {k: v for k, v in chunk.items() if k != "embedding"} for chunk in matching
        ]
    }

# LLM-based answer generation
@app.post("/api/answer", response_model=AnswerResponse)
def answer_question(request: AnswerRequest):
    if not vector_store:
        raise HTTPException(status_code=400, detail="Vector store is empty. Upload chunks first.")

    query_embedding = embed_text(request.query)
    scored_chunks = []

    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        if score >= request.min_score:
            scored_chunks.append({**item, "score": score})

    top_k = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)[:request.k]

    summary = summarize_chunks(request.query, [chunk["text"] for chunk in top_k])

    # 🧾 Generate answer in markdown format
    markdown_answer = f"### 🧠 Answer\n{summary}\n\n### 📚 Sources\n"
    for i, chunk in enumerate(top_k, start=1):
        markdown_answer += f"- [{i}] **{chunk['section_heading']}**, *{chunk['journal']}* ({chunk['publish_year']})\n"

    sources = [
        SearchResult(
            id=chunk["id"],
            text=chunk["text"],
            score=chunk["score"],
            source_doc_id=chunk["source_doc_id"],
            section_heading=chunk["section_heading"],
            journal=chunk["journal"],
            publish_year=chunk["publish_year"],
            attributes=chunk.get("attributes", {})
        )
        for chunk in top_k
    ]

    return AnswerResponse(answer=summary.strip(), sources=sources)
