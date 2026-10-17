import httpx
from .models import AgentMessage, MessageResponse

class AgentMailClient:
    """Обертка для MCP Agent Mail с использованием Pydantic."""

    def __init__(self, base_url: str = "http://127.0.0.1:8765"):
        self.base_url = base_url

    def send_message(self, message: AgentMessage) -> MessageResponse:
        """
        Отправляет сообщение агенту.
        Принимает AgentMessage, возвращает MessageResponse.
        """
        # Конвертируем модель Pydantic в словарь для отправки
        payload = message.model_dump()
        
        response = httpx.post(
            f"{self.base_url}/api/messages", 
            json=payload, 
            timeout=5.0
        )
        response.raise_for_status()
        
        # Валидируем ответ сервера через модель
        return MessageResponse(**response.json())
