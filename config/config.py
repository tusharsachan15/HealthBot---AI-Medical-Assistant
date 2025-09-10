import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the healthcare chatbot"""
    
    # API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    SERPER_API_KEY = os.getenv('SERPER_API_KEY', '')  # For web search
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '') 
    
    # Model configurations
    GROQ_MODEL = "mixtral-8x7b-32768"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # RAG settings
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    MAX_RETRIEVED_DOCS = 5
    
    # Response settings
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # File paths
    DOCUMENTS_PATH = "data/medical_documents/"
    VECTOR_STORE_PATH = "data/vector_store/"
    MEDICAL_CSV = "data/medical_knowledge.csv"
    DOCTORS_JSON = "data/doctors.json"
    
    # Web search settings
    SEARCH_RESULTS_LIMIT = 10
    
    @classmethod
    def validate_config(cls):
        """Validate that required API keys exist"""
        required_keys = ['GROQ_API_KEY']
        missing_keys = [key for key in required_keys if not getattr(cls, key)]
        
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        return True

# Streamlit UI settings
PAGE_CONFIG = {
    "page_title": "HealthBot - AI Medical Assistant",
    "page_icon": "🏥",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Healthcare-specific prompts
SYSTEM_PROMPTS = {
    "healthcare": """You are HealthBot, a knowledgeable AI medical assistant designed to help with healthcare queries. 
    
    IMPORTANT DISCLAIMERS:
    - Your responses are for informational purposes only
    - Always remind users to consult healthcare professionals
    - Never provide exact prescriptions or diagnoses
    - In emergencies, direct users to call local emergency services
    
    Your capabilities:
    - Explain diseases, symptoms, and treatments
    - Provide health tips and preventive care info
    - Explain medical terminology in simple language
    
    Always be empathetic, accurate, and responsible.""",
    
    "concise": "Provide concise, direct answers (2-3 sentences).",
    "detailed": "Provide comprehensive, detailed explanations with context and background information while maintaining medical accuracy and safety."
}
