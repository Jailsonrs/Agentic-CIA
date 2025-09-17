from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict
from agentic_cia.application.api.schemas.chat import ChatRequest, ChatResponse
from agentic_cia.application.chat_service_factory import get_chat_service_instance, available_services

router = APIRouter

@router.get("/services"):
    def list_services():
        return {"service": available_services()}

    def chat(req: ChatRequest):
        try:
            service = get_chat_service_instance(req.service)
        except ValueError as e:
            raise HTTPException(status_code = 400, details = str(e))
    
    response = service.generate_response(req.message, history)
    return(ChatResponse(response = response))