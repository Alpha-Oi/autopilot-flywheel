from pydantic import BaseModel
from autopilot_flywheel.observability.tracer import tracer

class ApprovalRequest(BaseModel):
    task_id: str
    command: str
    reason: str

class ApprovalGate:
    """Механизм запроса подтверждения у человека для опасных действий."""
    
    def __init__(self, auto_approve: bool = False):
        # В реальности здесь был бы вызов API/AgentMail.
        # Пока используем заглушку для тестов.
        self.auto_approve = auto_approve

    def request_approval(self, request: ApprovalRequest) -> bool:
        with tracer.start_as_current_span("hitl.request_approval") as span:
            span.set_attribute("task_id", request.task_id)
            span.set_attribute("command", request.command)
            
            if self.auto_approve:
                span.set_attribute("approved", True)
                return True
                
            # В будущем здесь будет отправка сообщения через AgentMail и ожидание ответа
            span.set_attribute("approved", False)
            return False
