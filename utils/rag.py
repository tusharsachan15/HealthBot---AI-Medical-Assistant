import os
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from config.config import Config
from models.embeddings import get_embedding_model

# -----------------------
# Load Documents
# -----------------------
def load_documents():
    """Load PDF/TXT medical documents from folder."""
    docs = []
    if not os.path.exists(Config.DOCUMENTS_PATH):
        return docs
    for file in os.listdir(Config.DOCUMENTS_PATH):
        path = os.path.join(Config.DOCUMENTS_PATH, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif file.endswith(".txt"):
            loader = TextLoader(path)
            docs.extend(loader.load())
    return docs

# -----------------------
# Build Vector Store
# -----------------------
def build_vector_store():
    docs = load_documents()
    if not docs:
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    embeddings = get_embedding_model()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(Config.VECTOR_STORE_PATH, exist_ok=True)
    vectorstore.save_local(Config.VECTOR_STORE_PATH)
    return vectorstore

# -----------------------
# Load Vector Store Safely
# -----------------------
def load_vector_store():
    embeddings = get_embedding_model()
    if os.path.exists(Config.VECTOR_STORE_PATH):
        # Allow loading our own saved vector store safely
        return FAISS.load_local(
            Config.VECTOR_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    return build_vector_store()

# -----------------------
# Truncate Text Cleanly
# -----------------------
def truncate_text(text, limit=300):
    """
    Truncate text without cutting words in half.
    """
    if len(text) <= limit:
        return text
    truncated = text[:limit]
    truncated = re.sub(r'\s+\S*$', '', truncated)
    return truncated + "..."

# -----------------------
# Retrieve Relevant Knowledge
# -----------------------
def retrieve(query):
    """
    Retrieve top-k relevant documents from vector store.
    Returns list of text chunks.
    """
    vectorstore = load_vector_store()
    if not vectorstore:
        return []

    results = vectorstore.similarity_search(query, k=Config.MAX_RETRIEVED_DOCS)

    # Convert to clean text
    clean_results = []
    for doc in results:
        text = doc.page_content if hasattr(doc, "page_content") else str(doc)
        # Clean extra whitespace and newlines
        text = " ".join(text.split())
        clean_results.append(text)

    return clean_results
