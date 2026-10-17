from hypothesis import given, strategies as st, settings
from autopilot_flywheel.safety.policy import PolicyEngine
from autopilot_flywheel.safety.dcg import DcgGuard

# Ограничиваем до 20 примеров, чтобы тесты были быстрыми
@settings(max_examples=20)
@given(st.text(min_size=1, max_size=100))
def test_policy_engine_fuzz(text):
    engine = PolicyEngine()
    result = engine.check(text)
    assert result.command == text

@settings(max_examples=10)
@given(st.text(min_size=1, max_size=100))
def test_dcg_guard_fuzz(text):
    guard = DcgGuard()
    result = guard.check_command(text)
    # Главное — не упасть, а вернуть валидный Pydantic-объект
    assert result.command == text
