import sys
import pytest
from autopilot_flywheel.main import main
from autopilot_flywheel.state.manager import StateManager

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
    monkeypatch.setattr(sys, "argv", ["main.py", "Build API", "--plan"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "🧠 Planning for request" in captured.out
    assert "✅ Created 2 tasks" in captured.out
    
    # Проверяем, что задачи реально записались в БД
    manager = StateManager()
    assert manager.get_state("task-1") is not None
