from fastapi import FastAPI
from agentic_cia.application.api.routers.chat import router as chat_router


app = FastAPI(title = 'Sac-RAG-C&A API')
app.include_router(chat_router, prefix = "/api", tags = ['chat'])
