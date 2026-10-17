import pytest
from autopilot_flywheel.safety.policy import PolicyEngine

@pytest.fixture
def engine():
    return PolicyEngine()

def test_policy_allow(engine):
    result = engine.check("git status")
    assert result.allowed is True

def test_policy_block(engine):
    result = engine.check("sudo apt update")
    assert result.allowed is False
    assert "Block sudo" in result.reason
