import pytest
from unittest.mock import patch
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.coordination.models import AgentMessage

def test_chaos_retry():
    client = AgentMailClient()
    msg = AgentMessage(sender="A", recipient="chaos_monkey", subject="S", body="B")
    
    # Мокаем _send_async, чтобы он выбрасывал ошибку (симуляция падения сети)
    with patch.object(AgentMailClient, "_send_async", side_effect=RuntimeError("Simulated network timeout")):
        with pytest.raises(RuntimeError, match="Simulated network timeout"):
            client.send_message(msg)
