from pydantic import BaseModel, Field

class AgentMessage(BaseModel):
    sender: str = Field(..., description="Имя агента-отправителя")
    recipient: str = Field(..., description="Имя агента-получателя")
    subject: str = Field(..., description="Тема сообщения")
    body: str = Field(..., description="Тело сообщения")

class MessageResponse(BaseModel):
    status: str
    message_id: int

class DcgResult(BaseModel):
    command: str = Field(..., description="Проверенная команда")
    allowed: bool = Field(..., description="True, если команда разрешена")
    reason: str | None = Field(None, description="Причина блокировки, если есть")
