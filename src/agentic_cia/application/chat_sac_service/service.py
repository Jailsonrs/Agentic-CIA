from typing import Optional, List, Dict
from agentic_cia.application.chat_service_base import ChatService
from agentic_cia.application.chat_sac_service.agent import qa_chain
from agentic_cia.application.chat_service_base import ChatService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatSacService(ChatService):

    def generate_response(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
         logger.info(f"Pergunta recebida: {message}")
         result = qa_chain.invoke(message)
         return result['result']

        
