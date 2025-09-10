from langchain_huggingface import HuggingFaceEmbeddings
from config.config import Config

def get_embedding_model():
    """Return embedding model for RAG"""
    return HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
