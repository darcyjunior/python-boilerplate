"""
Módulo principal da aplicação FastAPI.

Este é o ponto de entrada da aplicação, responsável por configurar e iniciar o servidor FastAPI,
além de incluir todos os roteadores e middlewares necessários.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from pathlib import Path

from .config import settings
from .api.v1.api import api_router as api_v1_router

# Configuração dos templates
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Cria a aplicação FastAPI
app = FastAPI(
    title="Boilerplate Python",
    description="""
    Um template moderno para projetos Python com FastAPI.
    
    ## Recursos
    - API RESTful com FastAPI
    - Documentação interativa (Swagger UI e ReDoc)
    - Autenticação JWT pronta para uso
    - Banco de dados com SQLAlchemy
    - Testes automatizados
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    # Configurações adicionais para melhorar a documentação
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "docExpansion": "none",
        "filter": True,
        "showExtensions": True,
    },
    # Tags para organização dos endpoints
    openapi_tags=[
        {
            "name": "todos",
            "description": "Operações com tarefas (To-Do items)",
        },
    ],
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Inclui os roteadores da API
app.include_router(api_v1_router, prefix="/api/v1")

# Rota para a página inicial
@app.get("/todos", response_class=HTMLResponse)
async def todos_page(request: Request):
    """Rota para a página de gerenciamento de tarefas."""
    return templates.TemplateResponse("todos.html", {"request": request})

# Tratamento global de erros de validação
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )

# Tratamento global de HTTPException para padronizar o formato de erro
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url.path),
            }
        },
    )

# Rota de saúde
@app.get(
    "/health",
    tags=["health"],
    summary="Verificar saúde da aplicação",
    description="Verifica se a API está funcionando corretamente.",
    response_description="Status da aplicação"
)
async def health_check():
    """
    Verifica a saúde da aplicação.
    
    Retorna um status 200 com uma mensagem de confirmação se a API estiver funcionando.
    """
    return {
        "status": "ok",
        "message": "API está funcionando corretamente",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
    }

# Rota raiz
@app.get(
    "/",
    tags=["root"],
    summary="Página inicial",
    description="Rota raiz da aplicação com informações básicas.",
    response_description="Mensagem de boas-vindas"
)
async def root():
    """
    Rota raiz da aplicação.
    
    Retorna informações básicas sobre a API e links para documentação.
    """
    return {
        "message": "Bem-vindo ao Boilerplate Python!",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi_schema": "/api/v1/openapi.json"
        },
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
    }
