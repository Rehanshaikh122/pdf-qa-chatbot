import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_pdf(pdf_path):
    """Extract text from PDF and split into chunks."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Split into small chunks (for embeddings)
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    return chunks

def create_faiss_index(chunks, index_dir="index"):
    """Create FAISS index from chunks."""
    embeddings = model.encode(chunks, convert_to_numpy=True)

    # FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index and chunks
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)

    faiss.write_index(index, os.path.join(index_dir, "faiss.index"))
    with open(os.path.join(index_dir, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)

def load_faiss_index(index_dir="index"):
    """Load FAISS index and chunks."""
    index = faiss.read_index(os.path.join(index_dir, "faiss.index"))
    with open(os.path.join(index_dir, "chunks.pkl"), "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def search_answer(query, index, chunks, top_k=3):
    """Search FAISS for best matching chunks."""
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = [chunks[i] for i in indices[0]]
    answer = " ".join(results)
    return answer, results
