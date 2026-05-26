import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(file_path="data/coaching_faq.txt"):
    """
    Data folder se text file load karta hai aur use small chunks mein split karta hai.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Bhai, {file_path} file nahi mili! Check karo.")
        
    loader = TextLoader(file_path, encoding='utf-8')
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"[SUCCESS] File loaded successfully. Total chunks: {len(chunks)}")
    return chunks

if __name__ == "__main__":
    # Test execution
    load_documents()