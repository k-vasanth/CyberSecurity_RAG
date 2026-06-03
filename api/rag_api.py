from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlite_utils.cli import query
from retrieval.retriever import Retriever
from context.context_builder import ContextBuilder
from generation.slm_generator import SLMGenerator

app = FastAPI()
retriever = Retriever()
context_builder = ContextBuilder()
generator = SLMGenerator()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "RAG API is running!"}

@app.get("/favicon.ico")
def get_favicon():
    return {"message": "No favicon available."}

@app.post("/ask")
def ask_rag(request: QueryRequest):

    query = request.query
    
    print("\n===== QUERY =====")
    print(query)

    retrieved_docs = retriever.retrieve(query=query,top_k=5)
    if not retrieved_docs:
        raise HTTPException(status_code=404, detail="No relevant documents found.")
    print("\n===== RETRIEVED DOCS =====")
    for doc in retrieved_docs:
        print(doc["metadata"]["url"])
    print("Retrieved docs count:", len(retrieved_docs))

    context = context_builder.build(retrieved_docs)
    print("\n===== BUILT CONTEXT =====")
    print(context[:2000])

    answer = generator.generate(query=query,context=context)
    print("\n===== GENERATED ANSWER =====")
    print(answer)

    references = []
    for doc in retrieved_docs:
        if ("metadata" in doc and "url" in doc["metadata"]):
            references.append(doc["metadata"]["url"])

    response = {
        "query": query,
        "answer": answer,
        "references": references
    }

    return response