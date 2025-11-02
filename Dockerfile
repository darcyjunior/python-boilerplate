# Estágio de build
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas o necessário para instalar as dependências
COPY pyproject.toml ./

# Criar ambiente virtual e instalar dependências
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install --no-cache-dir .[dev]

# Estágio final
FROM python:3.11-slim

# Instalar dependências de runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copiar o ambiente virtual do estágio de build
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Configurar variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app"

# Criar e configurar usuário não-root
RUN useradd -m appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Mudar para o usuário não-root
USER appuser
WORKDIR /app

# Copiar o código-fonte
COPY --chown=appuser:appuser . .

# Comando padrão
CMD ["python", "-m", "boilerplate"]
