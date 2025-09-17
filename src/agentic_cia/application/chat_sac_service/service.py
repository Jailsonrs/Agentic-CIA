from typing import Optional, List, Dict
from agentic_cia.application.chat_service_base import ChatService
from agentic_cia.application.chat_sac_service.agent import qa_chain
from agentic_cia.application.chat_service_base import ChatService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_formatted_response(response: str):
    """
    Recebe uma string e imprime no terminal com bullets e espaçamento.
    Cada linha da string vira um item.
    """
    print("\nResposta do chat:\n")
    for line in response.split("\n"):
        line = line.strip()
        if line:  # ignora linhas vazias
            print(f"• {line}\n")


class ChatSacService(ChatService):

    def generate_response(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
         logger.info(f"Pergunta recebida: {message}")
         result = qa_chain.invoke(message)
         print_formatted_response(result['result'])
         return result['result']
         #return result['result']

        
