"""
Endpoints para gerenciamento de Tarefas (To-Do).
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from boilerplate.models.todo import TodoCreate, TodoUpdate, TodoInDB
from boilerplate.services.todo import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=List[TodoInDB], summary="Listar tarefas")
async def read_todos():
    """
    Lista todas as tarefas cadastradas.
    
    Retorna uma lista com todas as tarefas existentes no sistema.
    """
    return await TodoService.get_todos()

@router.post(
    "/", 
    response_model=TodoInDB, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova tarefa"
)
async def create_todo(todo: TodoCreate):
    """
    Cria uma nova tarefa.
    
    - **title**: Título da tarefa (obrigatório)
    - **description**: Descrição detalhada (opcional)
    - **completed**: Status de conclusão (padrão: False)
    """
    return await TodoService.create_todo(todo.model_dump())

@router.get(
    "/{todo_id}", 
    response_model=TodoInDB,
    responses={
        404: {"description": "Tarefa não encontrada"}
    },
    summary="Obter tarefa por ID"
)
async def read_todo(todo_id: int):
    """
    Obtém os detalhes de uma tarefa específica.
    
    - **todo_id**: ID da tarefa a ser buscada
    """
    todo = await TodoService.get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    return todo

@router.put(
    "/{todo_id}", 
    response_model=TodoInDB,
    responses={
        404: {"description": "Tarefa não encontrada"}
    },
    summary="Atualizar tarefa"
)
async def update_todo(todo_id: int, todo: TodoUpdate):
    """
    Atualiza uma tarefa existente.
    
    - **todo_id**: ID da tarefa a ser atualizada
    - **title**: Novo título (opcional)
    - **description**: Nova descrição (opcional)
    - **completed**: Novo status de conclusão (opcional)
    """
    updated_todo = await TodoService.update_todo(todo_id, todo.model_dump(exclude_unset=True))
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    return updated_todo

@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Tarefa não encontrada"}
    },
    summary="Remover tarefa"
)
async def delete_todo(todo_id: int):
    """
    Remove uma tarefa do sistema.
    
    - **todo_id**: ID da tarefa a ser removida
    """
    if not await TodoService.delete_todo(todo_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    return {"ok": True}
