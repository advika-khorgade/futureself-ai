"""Configuration settings."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings."""
    
    # LLM Provider
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq").lower()
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.0"))
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Workflow Configuration
    MAX_RETRIES: int = 3
    TIMEOUT_SECONDS: int = 300
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required settings."""
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        if cls.LLM_PROVIDER == "groq" and not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required when using Groq provider. Get free key at: https://console.groq.com")
        if cls.LLM_PROVIDER == "huggingface_api" and not cls.HUGGINGFACE_API_KEY:
            raise ValueError("HUGGINGFACE_API_KEY is required when using HuggingFace API. Get free key at: https://huggingface.co/settings/tokens")
        return True
    
    @classmethod
    def get_provider_name(cls) -> str:
        """Get human-readable provider name."""
        names = {
            "openai": "OpenAI",
            "ollama": "Ollama (Local)",
            "huggingface": "HuggingFace (Local)",
            "groq": "Groq (Cloud - Free)",
            "huggingface_api": "HuggingFace API (Cloud - Free)"
        }
        return names.get(cls.LLM_PROVIDER, cls.LLM_PROVIDER.title())


settings = Settings()
