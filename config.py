import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Токен бота от @BotFather
    TELEGRAM_BOT_TOKEN: str = "7698382269:AAH46Q4RRHxY5m-yANSOyXDQmzRKP4EVVdw"
    
    # Если используете бесплатный Hugging Face API
    HUGGINGFACE_API_KEY: str = "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"
    OPENROUTER_API_KEY: str = "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" 
    GROQ_API_KEY: str = "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"
    # Модель для эмбеддингов (векторизации текста)
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    # Модель для генерации текста (используем меньшую модель для надежности)
    LLM_MODEL: str = "microsoft/DialoGPT-small"
    
    # Настройки БД - ИСПРАВЛЕННЫЙ ФОРМАТ
    DATABASE_URL: str = "mysql+mysqlconnector://root:kislyCat.03@localhost/economics"
    
    class Config:
        env_file = ".env"

settings = Settings()