import pytest
from unittest.mock import patch, MagicMock
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.coordination.models import AgentMessage

@pytest.fixture
def mail_client():
    return AgentMailClient()

@patch("httpx.post")
def test_send_message(mock_post, mail_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success", "message_id": 123}
    mock_post.return_value = mock_response

    # Создаем сообщение через Pydantic
    msg = AgentMessage(sender="AgentA", recipient="AgentB", subject="Task", body="Fix bug")
    result = mail_client.send_message(msg)

    # Проверяем, что вернулась Pydantic-модель
    assert result.status == "success"
    assert result.message_id == 123

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert "http://127.0.0.1:8765/api/messages" in args[0]
    assert kwargs["json"]["recipient"] == "AgentB"
