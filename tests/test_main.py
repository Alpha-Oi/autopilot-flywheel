import sys
import pytest
from autopilot_flywheel.main import main

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
    # DCG заблокирует эту команду независимо от YAML-политик
    monkeypatch.setattr(sys, "argv", ["main.py", "git reset --hard"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "❌ Command blocked" in captured.out
