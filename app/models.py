# app/models.py
from pydantic import BaseModel
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    ids: List[str]
    titles: Dict[str, str]