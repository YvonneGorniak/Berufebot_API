# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import QueryRequest, QueryResponse
from app.rag_query import run_query

app = FastAPI(title="FHDW RAG API")

# CORS offen für alle (du kannst später einschränken)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "FHDW RAG API läuft"}

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    return await run_query(req.question)