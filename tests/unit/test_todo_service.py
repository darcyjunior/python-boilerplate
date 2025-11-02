"""Testes unitários para o serviço de Tarefas."""
import pytest
import asyncio
from datetime import datetime
import pytz
from unittest.mock import Mock, patch, AsyncMock

# Importa os serviços reais do pacote instalado
from boilerplate.services.todo import TodoService, fake_db

class TestTodoService:
    """Testes para o serviço de Tarefas."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Configuração inicial para os testes."""
        # Limpa o banco de dados fake antes de cada teste
        fake_db.clear()
        self.service = TodoService()
        self.sample_todo = {
            "title": "Tarefa de teste",
            "description": "Descrição da tarefa de teste",
            "completed": False
        }
        self.timezone = pytz.timezone('America/Sao_Paulo')
        
    @pytest.fixture
    def event_loop(self):
        """Cria uma instância do loop de eventos para cada caso de teste."""
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
        
    @pytest.mark.asyncio
    async def test_create_todo_success(self):
        """Testa a criação de uma nova tarefa com sucesso."""
        result = await self.service.create_todo(self.sample_todo)
        
        assert result["title"] == self.sample_todo["title"]
        assert result["description"] == self.sample_todo["description"]
        assert result["completed"] == self.sample_todo["completed"]
        assert "id" in result
        assert "created_at" in result
        assert "updated_at" in result
        
        # Verifica se foi adicionado ao banco de dados
        assert len(fake_db) == 1
        assert fake_db[result["id"]] == result
    
    @pytest.mark.asyncio
    async def test_get_todo_found(self):
        """Testa a busca de uma tarefa existente por ID."""
        created = await self.service.create_todo(self.sample_todo)
        result = await self.service.get_todo(created["id"])
        
        assert result == created
    
    @pytest.mark.asyncio
    async def test_get_todo_not_found(self):
        """Testa a busca por um ID que não existe."""
        result = await self.service.get_todo(999)
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_todo_success(self):
        """Testa a atualização de uma tarefa existente."""
        created = await self.service.create_todo(self.sample_todo)
        update_data = {"title": "Título atualizado", "completed": True}
        
        with patch('boilerplate.services.todo.datetime') as mock_datetime:
            fixed_now = self.timezone.localize(datetime(2023, 1, 1, 12, 0, 0))
            mock_datetime.now.return_value = fixed_now
            
            result = await self.service.update_todo(created["id"], update_data)
            
            assert result["title"] == update_data["title"]
            assert result["completed"] == update_data["completed"]
            assert result["updated_at"] == fixed_now
    
    @pytest.mark.asyncio
    async def test_delete_todo_success(self):
        """Testa a exclusão de uma tarefa."""
        created = await self.service.create_todo(self.sample_todo)
        assert await self.service.delete_todo(created["id"]) is True
        assert len(fake_db) == 0
    
    @pytest.mark.asyncio
    async def test_get_todos(self):
        """Testa a listagem de tarefas."""
        # Cria tarefas de teste
        await self.service.create_todo({"title": "Tarefa 1", "completed": False, "description": ""})
        await self.service.create_todo({"title": "Tarefa 2", "completed": True, "description": ""})
        
        # Testa listar todas as tarefas
        all_todos = await self.service.get_todos()
        assert len(all_todos) == 2
        
        # Testa filtro implícito (todas as tarefas)
        all_todos_implicit = await self.service.get_todos()
        assert len(all_todos_implicit) == 2
