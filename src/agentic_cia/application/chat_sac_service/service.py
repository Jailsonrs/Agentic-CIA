from typing import Optional, List, Dict
from agentic_cia.application.chat_service_base import ChatService

class ChatSacService(ChatService):

    def generate_response(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
         logger.info(f"Pergunta recebida: {request.question}")
         result = qa_chain.invoke(request.question)
         return QueryResponse(answer=result["result"])

        
