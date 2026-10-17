import httpx
from .models import AgentMessage, MessageResponse
from autopilot_flywheel.observability.tracer import tracer

class AgentMailClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8765"):
        self.base_url = base_url

    def send_message(self, message: AgentMessage) -> MessageResponse:
        with tracer.start_as_current_span("agent_mail.send_message") as span:
            span.set_attribute("sender", message.sender)
            span.set_attribute("recipient", message.recipient)
            
            response = httpx.post(f"{self.base_url}/api/messages", json=message.model_dump(), timeout=5.0)
            response.raise_for_status()
            
            span.set_attribute("status_code", response.status_code)
            return MessageResponse(**response.json())
