import pytest
from autopilot_flywheel.prompts.planner_agent import PlannerAgent
from autopilot_flywheel.workers.worker_agent import WorkerAgent
from autopilot_flywheel.state.manager import StateManager

def test_worker_respects_dependencies(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    
    # 1. Создаем задачи
    planner = PlannerAgent()
    planner.plan("Test request")
    
    manager = StateManager()
    assert manager.get_state("task-1").status == "pending"
    assert manager.get_state("task-2").status == "pending"
    
    # 2. Запускаем воркер
    worker = WorkerAgent()
    worker.run()
    
    # 3. Проверяем, что обе задачи выполнены в правильном порядке
    assert manager.get_state("task-1").status == "completed"
    assert manager.get_state("task-2").status == "completed"
    
    # Проверяем вывод консоли (task-1 должен быть первым)
    captured = capsys.readouterr()
    assert "Create API skeleton" in captured.out
    assert "Implement auth" in captured.out
    # Убеждаемся, что auth не выполнялся раньше skeleton
    assert captured.out.find("Create API") < captured.out.find("Implement auth")
