from fastapi import FastAPI
from pydantic import BaseModel
from utils import load_pdf, create_faiss_index, load_faiss_index, search_answer
import uvicorn
import os

PDF_PATH = "data/manual.pdf"
INDEX_DIR = "index"

# Create FAISS index if it doesn't exist
try:
    index, chunks = load_faiss_index(INDEX_DIR)
except:
    chunks = load_pdf(PDF_PATH)
    create_faiss_index(chunks, INDEX_DIR)
    index, chunks = load_faiss_index(INDEX_DIR)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(req: QueryRequest):
    answer, sources = search_answer(req.query, index, chunks)
    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    # Bind to 0.0.0.0 so public internet can access it
    # Use Render's assigned PORT or default to 10000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
