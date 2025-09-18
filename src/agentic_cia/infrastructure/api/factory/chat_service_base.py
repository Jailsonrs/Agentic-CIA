from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class ChatService(ABC):

    @abstractmethod
    def generate_response(self, message:str, history: Optional[List[Dict[str, str]]] = None) -> str:
        pass

    