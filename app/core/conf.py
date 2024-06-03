from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

BasePath = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    """Global Settings"""
    
    model_config = SettingsConfigDict(env_file=f'{BasePath}/.env', env_file_encoding='utf-8', extra='ignore')
    
    # Env Openai
    OPENAI_API_KEY1: str
    OPENAI_API_KEY2: str
    OPENAI_API_KEY3: str
    
    # Google Services
    GOOGLE_EMAIL: str
    
    # FastAPI
    API_V1_STR: str = '/api/chatbot/v1'
    TITLE: str = "Chatbot API"
    VERSION: str = "0.0.1"
    DOCS_URL: str|None = f'{API_V1_STR}/docs'
    REDOCS_URL: str|None = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str|None = f'{API_V1_STR}/openapi'
    
    # ChromaDB
    
    # MongoDB
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_DATABASE: str
    MONGODB_COLLECTION: str
    

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()