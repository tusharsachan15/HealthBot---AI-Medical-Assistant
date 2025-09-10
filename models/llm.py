import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langchain_groq import ChatGroq
from config.config import Config

def get_chatgroq_model():
    """Initialize and return the Groq chat model"""
    try:
        model = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model=Config.GROQ_MODEL,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS
        )
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")


