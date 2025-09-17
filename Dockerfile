# Base image
FROM python:3.12-slim

# Instala o UV (Universal Virtualenv)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Diretório de trabalho
WORKDIR /app

# Copia dependências para instalação
COPY uv.lock pyproject.toml README.md ./

# Cria virtualenv e instala dependências
RUN uv sync --frozen --no-cache

# Copia o código da aplicação
COPY src/agentic_cia ./agentic_cia
COPY data ./data
COPY chroma_sac ./chroma_sac
COPY static ./static

# Configura variáveis de ambiente
ENV OLLAMA_HOST=http://ollama:11434
ENV REDIS_HOST=redis
ENV PYTHONUNBUFFERED=1

# Exposição de portas
EXPOSE 8000

# Define volumes para persistência de dados
VOLUME ["/app/chroma_sac", "/app/data", "/app/static"]

# Comando de execução da aplicação
CMD ["/app/.venv/bin/uvicorn", "agentic_cia.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
