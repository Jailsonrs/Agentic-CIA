from typing import Dict, Type, List
from agentic_cia.application.chat_service_base import ChatService
from agentic_cia.application.chat_a_service.service import ChatAService
from agentic_cia.application.chat_b_service.service import ChatBService


_registry: Dict[str, Type[ChatService]] = {
    "chat_sac": ChatSacService,
    "chat_prod": ChatProdService,
}


def available_services() -> List[str]:
    return list(_registry.keys())

def get_chat_service_instance(name: str) -> ChatService:
    try:
        cls = _registry[name]
    except KeyError:
        raise ValueError(f"Serviço '{name}' não encontrado.")
    return cls()

