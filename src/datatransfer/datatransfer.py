import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Document loaders
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    BSHTMLLoader,
    Docx2txtLoader
)

# Text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Vector DB
from langchain_community.vectorstores import FAISS


# -----------------------------
# Load documents from folder
# -----------------------------
def load_documents(data_path):

    docs = []

    for file in Path(data_path).glob("*"):

        suffix = file.suffix.lower()

        if suffix == ".pdf":
            loader = PyMuPDFLoader(str(file))

        elif suffix == ".txt":
            loader = TextLoader(str(file))

        elif suffix == ".html":
            loader = BSHTMLLoader(str(file))

        elif suffix == ".docx":
            loader = Docx2txtLoader(str(file))

        else:
            continue

        documents = loader.load()
        docs.extend(documents)

    return docs


# -----------------------------
# Create chunks
# -----------------------------
def create_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    return chunks


# -----------------------------
# Main Pipeline
# -----------------------------
def main():

    # Load documents
    documents = load_documents("data")

    print(f"Loaded {len(documents)} documents")

    # Split into chunks
    chunks = create_chunks(documents)

    print(f"Created {len(chunks)} chunks")

    # Embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Vector DB folder
    BASE_DIR = Path.cwd()
    save_path = BASE_DIR / "embeddings"
    save_path.mkdir(parents=True, exist_ok=True)

    # Create FAISS DB
    db = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    db.save_local(save_path)

    print("Vector database saved successfully")


# Run
if __name__ == "__main__":
    main()