import pytest
from autopilot_flywheel.prompts.planner_agent import PlannerAgent
from autopilot_flywheel.prompts.task_models import TaskNode
from autopilot_flywheel.state.manager import StateManager

def test_planner_creates_tasks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    agent = PlannerAgent()
    
    graph = agent.plan("Build a REST API")
    
    assert len(graph.tasks) == 2
    assert graph.tasks[0].id == "task-1"
    
    manager = StateManager()
    t1 = manager.get_state("task-1")
    t2 = manager.get_state("task-2")
    
    assert t1.status == "pending"
    
    # Проверяем, что в payload лежит валидный JSON (модель TaskNode)
    node1 = TaskNode.model_validate_json(t1.payload)
    assert node1.description == "Create API skeleton"
    assert node1.blocks == []
    
    node2 = TaskNode.model_validate_json(t2.payload)
    assert node2.blocks == ["task-1"]
