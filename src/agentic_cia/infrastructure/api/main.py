from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from agentic_cia.infrastructure.db import base, database, orm_models
from agentic_cia.infrastructure.api.models import ChatRequest, ChatResponse
from agentic_cia.application.orchestrator import handle_message

# criar tabelas
base.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Agentic CIA - Chat API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chat/{session_id}", response_model=ChatResponse)
def chat(session_id: int, request: ChatRequest, db: Session = Depends(get_db)):
    response = handle_message(db, session_id, request.message)
    return response

@app.get("/")
def root():
    return {"message": "🚀 Agentic CIA API online"}
