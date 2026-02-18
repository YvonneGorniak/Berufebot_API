# app/rag_config.py
import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient, AsyncQdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import (
    Settings,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import get_response_synthesizer

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

SYSTEM_PROMPT = """<-- Dein Prompt 1:1 übernommen -->"""

llm = OpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=1,
    max_completion_tokens=2048,
    system_prompt=SYSTEM_PROMPT,
)

embed_model = HuggingFaceEmbedding(
    model_name="intfloat/multilingual-e5-small"
)

Settings.llm = llm
Settings.embed_model = embed_model

client = QdrantClient(
    url="https://d1781b00-d416-479a-819c-8d8035761f26.europe-west3-0.gcp.cloud.qdrant.io",
    api_key=QDRANT_API_KEY,
)

aclient = AsyncQdrantClient(
    url="https://d1781b00-d416-479a-819c-8d8035761f26.europe-west3-0.gcp.cloud.qdrant.io",
    api_key=QDRANT_API_KEY,
)

collection_name = "FHDW"

vector_store = QdrantVectorStore(
    client=client, aclient=aclient,
    collection_name=collection_name,
    prefer_grpc=False,
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context
)

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=15,
    similarity_cutoff=0.6,
)

response_synthesizer = get_response_synthesizer(
    llm=llm,
    streaming=False
)

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)