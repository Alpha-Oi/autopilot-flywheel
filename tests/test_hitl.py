import pytest
from autopilot_flywheel.safety.hitl import ApprovalGate, ApprovalRequest

def test_auto_approve():
    gate = ApprovalGate(auto_approve=True)
    req = ApprovalRequest(task_id="t1", command="rm -rf /", reason="Test")
    assert gate.request_approval(req) is True

def test_manual_block():
    gate = ApprovalGate(auto_approve=False)
    req = ApprovalRequest(task_id="t1", command="rm -rf /", reason="Test")
    assert gate.request_approval(req) is False
