"""Testes de integração para a API de Tarefas."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import json

# Importa o aplicativo FastAPI do pacote instalado
from boilerplate.main import app

class TestTodoAPI:
    """Testes para os endpoints da API de Tarefas."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Configuração inicial para os testes."""
        self.client = TestClient(app)
        self.base_url = "/api/v1/todos"
        self.sample_todo = {
            "title": "Tarefa de teste API",
            "description": "Descrição da tarefa de teste API",
            "completed": False
        }
    
    def _create_todo(self):
        response = self.client.post(
            f"{self.base_url}",
            json=self.sample_todo
        )
        assert response.status_code == 201
        return response.json()
        
    def test_create_todo_success(self):
        """Testa a criação de uma tarefa via API."""
        data = self._create_todo()
        # Verifica se os dados retornados estão corretos
        assert data["title"] == self.sample_todo["title"]
        assert data["description"] == self.sample_todo["description"]
        assert data["completed"] == self.sample_todo["completed"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_get_todo_by_id(self):
        """Testa a busca de uma tarefa por ID via API."""
        # Primeiro cria uma tarefa
        created = self._create_todo()
        
        # Agora busca pelo ID
        response = self.client.get(f"{self.base_url}/{created['id']}")
        assert response.status_code == 200
        
        # Verifica se os dados retornados são iguais aos criados
        data = response.json()
        assert data == created
    
    def test_update_todo(self):
        """Testa a atualização de uma tarefa via API."""
        # Cria uma tarefa
        created = self._create_todo()
        
        # Atualiza a tarefa
        update_data = {"title": "Título Atualizado", "completed": True}
        response = self.client.put(
            f"{self.base_url}/{created['id']}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verifica se os dados foram atualizados corretamente
        assert data["title"] == update_data["title"]
        assert data["completed"] == update_data["completed"]
        assert data["id"] == created["id"]
        assert "updated_at" in data
        assert data["updated_at"] != created["updated_at"]  # Deve ter sido atualizado
    
    def test_delete_todo(self):
        """Testa a exclusão de uma tarefa via API."""
        # Cria uma tarefa
        created = self._create_todo()
        
        # Exclui a tarefa (API retorna 204 No Content)
        response = self.client.delete(f"{self.base_url}/{created['id']}")
        assert response.status_code == 204
        assert response.content == b""
        
        # Verifica se realmente foi excluída
        response = self.client.get(f"{self.base_url}/{created['id']}")
        assert response.status_code == 404
        
        # Tenta excluir novamente (deve retornar 404)
        response = self.client.delete(f"{self.base_url}/{created['id']}")
        assert response.status_code == 404
    
    def test_list_todos(self):
        """Testa a listagem de tarefas e a consistência após atualizações."""
        # Cria três tarefas
        created_todos = [self._create_todo() for _ in range(3)]
        
        # Marca duas como concluídas
        update_true = {"completed": True}
        self.client.put(f"{self.base_url}/{created_todos[0]['id']}", json=update_true)
        self.client.put(f"{self.base_url}/{created_todos[1]['id']}", json=update_true)
        
        # Busca todas as tarefas
        response = self.client.get(f"{self.base_url}")
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) >= 3  # Pode haver interferência de outros testes
        
        # Conta concluídas e pendentes a partir do retorno atual
        completed_count = sum(1 for t in todos if t.get("completed") is True)
        pending_count = sum(1 for t in todos if t.get("completed") is False)
        assert completed_count >= 2
        assert pending_count >= 1
