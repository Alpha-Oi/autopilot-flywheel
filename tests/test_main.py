import sys
import pytest
from autopilot_flywheel.main import main
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.prompts.llm_client import LLMClient

def test_main_safe(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["main.py", "git status"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "✅ Command allowed" in captured.out

def test_main_blocked(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["main.py", "git reset --hard"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "❌ Command blocked" in captured.out

def test_main_plan(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    # Подменяем метод generate у LLMClient, чтобы не ходить в сеть
    monkeypatch.setattr(LLMClient, "generate", lambda *args, **kwargs: """
        {
          "tasks": [
            {"id": "task-1", "description": "Test task 1", "blocks": []},
            {"id": "task-2", "description": "Test task 2", "blocks": ["task-1"]}
          ]
        }
    """)
    
    monkeypatch.setattr(sys, "argv", ["main.py", "Build API", "--plan"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "🧠 Planning for request" in captured.out
    assert "✅ Created 2 tasks" in captured.out
    
    manager = StateManager()
    assert manager.get_state("task-1") is not None
