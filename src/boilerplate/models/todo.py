"""
Modelos Pydantic para a API de Tarefas (To-Do).
"""
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
import pytz
from ..config import settings

class TodoBase(BaseModel):
    """Modelo base para Tarefa."""
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    """Modelo para criação de Tarefa."""
    pass

class TodoUpdate(BaseModel):
    """Modelo para atualização de Tarefa."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoInDB(TodoBase):
    """Modelo para Tarefa no banco de dados."""
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(pytz.timezone(settings.TIMEZONE)))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(pytz.timezone(settings.TIMEZONE)))

    # Configuração Pydantic v2
    model_config = ConfigDict(from_attributes=True)

    @field_validator('created_at', 'updated_at')
    def ensure_timezone(cls, v):
        """Garante que as datas tenham o timezone correto."""
        if v.tzinfo is None:
            return v.replace(tzinfo=pytz.timezone(settings.TIMEZONE))
        return v.astimezone(pytz.timezone(settings.TIMEZONE))

    # A serialização de datetime já é ISO 8601 por padrão no FastAPI/Pydantic v2,
    # então não é necessário definir json_encoders personalizados.
