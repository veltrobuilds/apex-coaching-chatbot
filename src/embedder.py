import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.loader import load_documents

VECTOR_STORE_PATH = "faiss_index"

def get_embeddings():
    """Get HuggingFace embeddings model without meta-tensor issues."""
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
        # model_kwargs ko hata diya taaki torch device initialization conflict na kare
    )

def create_vector_store(file_path: str):
    """Create FAISS vector store from documents."""
    chunks = load_documents(file_path)
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)
    return vector_store

def load_vector_store():
    """Load existing FAISS vector store."""
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store

def get_or_create_vector_store(file_path: str):
    """Load existing or create new vector store based on local path."""
    if os.path.exists(VECTOR_STORE_PATH):
        print("[INFO] Loading existing FAISS index from local disk...")
        return load_vector_store()
    print("[INFO] Creating fresh FAISS vector store...")
    return create_vector_store(file_path)