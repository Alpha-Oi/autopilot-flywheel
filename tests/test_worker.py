import pytest
from unittest.mock import MagicMock
from autopilot_flywheel.prompts.planner_agent import PlannerAgent
from autopilot_flywheel.workers.worker_agent import WorkerAgent
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.coordination.models import MessageResponse

class MockLLMClient:
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return """
        {
          "tasks": [
            {"id": "task-1", "description": "Create API skeleton", "blocks": []},
            {"id": "task-2", "description": "Implement auth", "blocks": ["task-1"]}
          ]
        }
        """

def test_worker_respects_dependencies(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    
    # Подменяем AgentMailClient, чтобы не слать реальные запросы
    mock_mail = MagicMock()
    mock_mail.send_message.return_value = MessageResponse(status="success", message_id=1)
    
    planner = PlannerAgent(llm_client=MockLLMClient())
    planner.plan("Test request")
    
    manager = StateManager()
    assert manager.get_state("task-1").status == "pending"
    assert manager.get_state("task-2").status == "pending"
    
    worker = WorkerAgent(mail_client=mock_mail)
    worker.run()
    
    assert manager.get_state("task-1").status == "completed"
    assert manager.get_state("task-2").status == "completed"
    
    captured = capsys.readouterr()
    assert captured.out.find("Create API") < captured.out.find("Implement auth")
    # Проверяем, что было отправлено 2 уведомления
    assert mock_mail.send_message.call_count == 2
