# app/rag_query.py
from app.rag_config import query_engine
from app.professions import extract_ids_from_resp, fetch_titles_for_ids

async def run_query(question: str):
    resp = await query_engine.aquery(question)
    answer = str(resp)

    ids = extract_ids_from_resp(resp)
    titles = await fetch_titles_for_ids(ids)

    return {
        "answer": answer,
        "ids": ids,
        "titles": titles,
    }