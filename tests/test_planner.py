import pytest
from autopilot_flywheel.prompts.planner_agent import PlannerAgent
from autopilot_flywheel.state.manager import StateManager

def test_planner_creates_tasks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Инициализируем агента (он создаст временную БД)
    agent = PlannerAgent()
    
    # Запускаем планирование
    graph = agent.plan("Build a REST API")
    
    # Проверяем, что вернулся граф
    assert len(graph.tasks) == 2
    assert graph.tasks[0].id == "task-1"
    
    # Проверяем, что задачи сохранились в БД
    manager = StateManager()
    t1 = manager.get_state("task-1")
    t2 = manager.get_state("task-2")
    
    assert t1.status == "pending"
    assert t1.payload == "Create API skeleton"
    assert t2.status == "pending"
