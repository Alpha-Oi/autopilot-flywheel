import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .models import AgentMessage, MessageResponse
from autopilot_flywheel.observability.tracer import tracer

class AgentMailClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8765"):
        self.base_url = base_url

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.1, min=0.1, max=1),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException)),
        reraise=True
    )
    def send_message(self, message: AgentMessage) -> MessageResponse:
        with tracer.start_as_current_span("agent_mail.send_message") as span:
            span.set_attribute("sender", message.sender)
            span.set_attribute("recipient", message.recipient)
            
            if message.recipient == "chaos_monkey":
                raise httpx.TimeoutException("Simulated network timeout")

            response = httpx.post(f"{self.base_url}/api/messages", json=message.model_dump(), timeout=5.0)
            response.raise_for_status()
            return MessageResponse(**response.json())
