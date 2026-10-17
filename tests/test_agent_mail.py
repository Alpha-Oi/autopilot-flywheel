import pytest
from unittest.mock import patch, MagicMock
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.coordination.models import AgentMessage, MessageResponse

@pytest.fixture
def mail_client():
    return AgentMailClient()

@patch.object(AgentMailClient, "_send_async")
def test_send_message(mock_send_async, mail_client):
    mock_send_async.return_value = MessageResponse(status="success", message_id=123)
    
    msg = AgentMessage(sender="AgentA", recipient="AgentB", subject="Task", body="Fix bug")
    result = mail_client.send_message(msg)
    
    assert result.status == "success"
    assert result.message_id == 123
    mock_send_async.assert_called_once()
