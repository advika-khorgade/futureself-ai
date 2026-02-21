"""LLM factory for creating language model instances."""
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
from config import settings


def create_llm(model_name: str = None, temperature: float = None):
    """
    Create an LLM instance based on configuration.
    
    Args:
        model_name: Override model name (uses settings default if None)
        temperature: Override temperature (uses settings default if None)
        
    Returns:
        LLM instance
    """
    model = model_name or settings.MODEL_NAME
    temp = temperature if temperature is not None else settings.TEMPERATURE
    
    if settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model=model,
            temperature=temp
        )
    
    elif settings.LLM_PROVIDER == "groq":
        return ChatGroq(
            model=model,
            temperature=temp,
            groq_api_key=settings.GROQ_API_KEY
        )
    
    elif settings.LLM_PROVIDER == "huggingface_api":
        from langchain_community.llms import HuggingFaceHub
        return HuggingFaceHub(
            repo_id=model,
            model_kwargs={
                "temperature": temp,
                "max_length": 512
            },
            huggingfacehub_api_token=settings.HUGGINGFACE_API_KEY
        )
    
    elif settings.LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=model,
            temperature=temp,
            base_url=settings.OLLAMA_BASE_URL
        )
    
    else:
        raise ValueError(
            f"Unsupported LLM provider: {settings.LLM_PROVIDER}. "
            "Use 'openai', 'groq', 'huggingface_api', or 'ollama'"
        )
