import pytest
import httpx
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.coordination.models import AgentMessage

def test_chaos_retry():
    client = AgentMailClient()
    msg = AgentMessage(sender="A", recipient="chaos_monkey", subject="S", body="B")
    with pytest.raises(httpx.TimeoutException):
        client.send_message(msg)
