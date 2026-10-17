import pytest
from autopilot_flywheel.orchestrator import AutopilotOrchestrator

@pytest.fixture
def orchestrator(tmp_path, monkeypatch):
    # Безопасно меняем директорию для теста. 
    # Pytest (monkeypatch) сам вернет её обратно после завершения теста.
    monkeypatch.chdir(tmp_path)
    return AutopilotOrchestrator()

def test_orchestrator_allow_safe(orchestrator):
    assert orchestrator.process_command("t1", "git status") is True

def test_orchestrator_block_policy(orchestrator):
    # Команда с sudo должна быть заблокирована политикой
    assert orchestrator.process_command("t2", "sudo rm -rf /") is False

def test_orchestrator_block_dcg(orchestrator):
    # Команда git reset --hard должна быть заблокирована DCG
    assert orchestrator.process_command("t3", "git reset --hard") is False
