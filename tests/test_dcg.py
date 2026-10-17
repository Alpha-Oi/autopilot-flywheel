import pytest
from autopilot_flywheel.safety.dcg import DcgGuard

@pytest.fixture
def guard():
    return DcgGuard()

def test_safe_command(guard):
    assert guard.check_command("git status") is True

def test_destructive_command(guard):
    assert guard.check_command("git reset --hard HEAD~5") is False
