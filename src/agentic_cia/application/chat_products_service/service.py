from typing import Optional, List, Dict
from agentic_cia.application.chat_service_base import ChatService


class ChatProdService(ChatService):

    def generate_response(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        return "mensagem"
        