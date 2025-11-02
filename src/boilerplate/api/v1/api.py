"""
Módulo principal da API v1.

Este módulo é responsável por configurar e incluir todos os roteadores da API v1.
"""
from fastapi import APIRouter

# Importe os roteadores aqui
from .endpoints import todos

# Cria o roteador principal da API v1
api_router = APIRouter()

# Inclui os roteadores de cada recurso
api_router.include_router(todos.router)
