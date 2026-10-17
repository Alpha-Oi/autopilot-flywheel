import httpx

class AgentMailClient:
    """Обертка для MCP Agent Mail."""

    def __init__(self, base_url: str = "http://127.0.0.1:8765"):
        self.base_url = base_url

    def send_message(self, sender: str, recipient: str, subject: str, body: str) -> dict:
        """
        Отправляет сообщение агенту.
        Возвращает ответ сервера в виде словаря.
        """
        payload = {
            "sender": sender,
            "recipient": recipient,
            "subject": subject,
            "body": body
        }
        
        # Отправляем POST-запрос на сервер
        response = httpx.post(
            f"{self.base_url}/api/messages", 
            json=payload, 
            timeout=5.0
        )
        response.raise_for_status()
        return response.json()
