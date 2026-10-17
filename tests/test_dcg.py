import pytest
from autopilot_flywheel.safety.dcg import DcgGuard

@pytest.fixture
def guard():
    return DcgGuard()

def test_safe_command(guard):
    result = guard.check_command("git status")
    assert result.allowed is True
    assert result.command == "git status"

def test_destructive_command(guard):
    result = guard.check_command("git reset --hard HEAD~5")
    assert result.allowed is False
    assert result.reason is not None
