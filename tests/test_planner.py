import pytest
from autopilot_flywheel.prompts.planner_agent import PlannerAgent
from autopilot_flywheel.prompts.task_models import TaskNode
from autopilot_flywheel.state.manager import StateManager

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

def test_planner_creates_tasks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    # Передаем фейковый LLM, чтобы тест не ходил в сеть
    mock_llm = MockLLMClient()
    agent = PlannerAgent(llm_client=mock_llm)
    
    graph = agent.plan("Build a REST API")
    
    assert len(graph.tasks) == 2
    assert graph.tasks[0].id == "task-1"
    
    manager = StateManager()
    t1 = manager.get_state("task-1")
    
    assert t1.status == "pending"
    node1 = TaskNode.model_validate_json(t1.payload)
    assert node1.description == "Create API skeleton"
