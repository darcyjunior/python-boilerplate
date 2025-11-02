"""
Serviço para gerenciamento de Tarefas (To-Do).
"""
from typing import List, Optional
from datetime import datetime
import pytz
from ..config import settings

# Banco de dados em memória para exemplo
fake_db = {}
id_counter = 1

class TodoService:
    """Serviço para operações relacionadas a Tarefas."""
    
    @staticmethod
    async def get_todos() -> List[dict]:
        """Retorna todas as tarefas."""
        return list(fake_db.values())

    @staticmethod
    async def get_todo(todo_id: int) -> Optional[dict]:
        """Obtém uma tarefa pelo ID."""
        return fake_db.get(todo_id)

    @staticmethod
    async def create_todo(todo_data: dict) -> dict:
        """Cria uma nova tarefa."""
        global id_counter
        todo_id = id_counter
        timezone = pytz.timezone(settings.TIMEZONE)
        now = datetime.now(timezone)
        todo = {
            "id": todo_id,
            **todo_data,
            "created_at": now,
            "updated_at": now
        }
        fake_db[todo_id] = todo
        id_counter += 1
        return todo

    @staticmethod
    async def update_todo(todo_id: int, todo_data: dict) -> Optional[dict]:
        """Atualiza uma tarefa existente."""
        if todo_id not in fake_db:
            return None
        
        # Remove valores None para atualização parcial
        update_data = {k: v for k, v in todo_data.items() if v is not None}
        
        timezone = pytz.timezone(settings.TIMEZONE)
        fake_db[todo_id].update({
            **update_data,
            "updated_at": datetime.now(timezone)
        })
        return fake_db[todo_id]

    @staticmethod
    async def delete_todo(todo_id: int) -> bool:
        """Remove uma tarefa."""
        if todo_id in fake_db:
            del fake_db[todo_id]
            return True
        return False
