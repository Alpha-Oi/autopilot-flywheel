import pytest
from unittest.mock import MagicMock, patch
from autopilot_flywheel.prompts.planner_agent import PlannerAgent
from autopilot_flywheel.workers.worker_agent import WorkerAgent
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.coordination.models import MessageResponse

class MockLLMClient:
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return """
        {
          "tasks": [
            {"id": "task-1", "description": "Create API directory", "blocks": [], "command": "mkdir api"},
            {"id": "task-2", "description": "Create auth file", "blocks": ["task-1"], "command": "echo test > api/auth.py"}
          ]
        }
        """

@patch("subprocess.run")
def test_worker_executes_commands(mock_subprocess, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mock_subprocess.return_value.returncode = 0
    mock_subprocess.return_value.stdout = "Mocked output"
    
    planner = PlannerAgent(llm_client=MockLLMClient())
    planner.plan("Build API")
    
    mock_mail = MagicMock()
    mock_mail.send_message.return_value = MessageResponse(status="success", message_id=1)
    
    worker = WorkerAgent(mail_client=mock_mail)
    worker.run()
    
    manager = StateManager()
    assert manager.get_state("task-1").status == "completed"
    assert manager.get_state("task-2").status == "completed"
    
    # 4 вызова: 2 для DCG-проверки, 2 для реального выполнения
    assert mock_subprocess.call_count == 4
    
    # Проверяем, что реальные команды были среди вызовов
    all_calls = [str(call) for call in mock_subprocess.call_args_list]
    assert any("mkdir api" in c for c in all_calls)
    assert any("echo test" in c for c in all_calls)
