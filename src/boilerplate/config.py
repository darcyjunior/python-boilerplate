"""
Módulo de configuração da aplicação.
"""
import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # Configurações básicas
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    APP_NAME: str = "Boilerplate Python"
    VERSION: str = "0.1.0"
    SECRET_KEY: str = "your-secret-key-here"
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Configurações do banco de dados
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"

    # Configurações de segurança
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 dias
    ALGORITHM: str = "HS256"

    # Configurações de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configurações de cache
    CACHE_TTL: int = 300  # 5 minutos

    # Configurações de e-mail
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@example.com"

    # Configurações de armazenamento
    STORAGE_BACKEND: str = "local"  # ou 's3', 'gcs', etc.
    STORAGE_BUCKET: str = ""
    STORAGE_PREFIX: str = ""
    
    # Configuração de timezone
    TIMEZONE: str = "America/Sao_Paulo"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Validadores
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info):
        env = info.data.get("ENVIRONMENT", "development")
        if env == "production" and (not v or v == "your-secret-key-here"):
            raise ValueError("SECRET_KEY deve ser configurada em produção")
        return v

    @field_validator("TIMEZONE")
    @classmethod
    def validate_timezone(cls, v: str):
        import pytz
        try:
            pytz.timezone(v)
            return v
        except Exception:
            # Fallback seguro
            return "America/Sao_Paulo"


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna as configurações da aplicação.
    
    Utiliza lru_cache para evitar a recriação das configurações a cada requisição.
    Configura o timezone para America/Sao_Paulo.
    """
    # Importa os módulos necessários
    import os
    import time
    import pytz
    from datetime import datetime
    
    # Obtém as configurações
    settings = Settings()
    
    # Configura o timezone do sistema operacional
    os.environ["TZ"] = settings.TIMEZONE
    
    try:
        time.tzset()  # Linux/Unix
    except AttributeError:
        # Windows não tem time.tzset()
        pass  # Já configuramos o TZ anteriormente
        
    # Configura o timezone padrão para o pytz
    timezone = pytz.timezone(settings.TIMEZONE)
    datetime.now(timezone)  # Aplica o timezone
    
    return settings

# Instância global de configurações
settings = get_settings()
