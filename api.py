from fastapi import FastAPI, HTTPException
from uuid import uuid4
from embedding import embed_text
from models import Chunk, UploadRequest, SimilaritySearchRequest, SearchResult
from vector_utils import vector_store, cosine_similarity

from llm import generate_answer
from models import AnswerRequest, AnswerResponse

app = FastAPI()

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

@app.post("/api/similarity_search", response_model=list[SearchResult])
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


### LLM Integration ###

@app.post("/api/answer", response_model=AnswerResponse)
def answer_question(request: AnswerRequest):
    if not vector_store:
        raise HTTPException(status_code=400, detail="Vector store is empty. Upload chunks first.")

    query_embedding = embed_text(request.query)

    # Find the best k chunks
    scored_results = []
    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        if score >= request.min_score:
            scored_results.append({**item, "score": score})
    top_k = sorted(scored_results, key=lambda x: x["score"], reverse=True)[:request.k]

    # Generate the prompt
    excerpts = "\n\n".join(
        [f"{i+1}. {chunk['text']}" for i, chunk in enumerate(top_k)]
    )
    prompt = f"""
You are a helpful scientific assistant. Answer the following question using ONLY the provided excerpts below. Use citations like [1], [2] as needed.

QUESTION:
{request.query}

EXCERPTS:
{excerpts}

ANSWER:
""".strip()

    # Generate answer
    answer = generate_answer(prompt)

    # Return the best k chunks with answer
    sources = [
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

    return AnswerResponse(answer=answer.strip(), sources=sources)