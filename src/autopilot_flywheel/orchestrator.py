from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState
from autopilot_flywheel.safety.policy import PolicyEngine
from autopilot_flywheel.safety.dcg import DcgGuard
from autopilot_flywheel.observability.tracer import tracer

class AutopilotOrchestrator:
    """Главный дирижер, управляющий жизненным циклом задач."""
    
    def __init__(self):
        self.state_manager = StateManager()
        self.policy_engine = PolicyEngine()
        self.dcg_guard = DcgGuard()

    def process_command(self, task_id: str, command: str) -> bool:
        """
        Обрабатывает команду агента: проверяет политики, DCG и сохраняет состояние.
        Возвращает True, если команда разрешена к выполнению.
        """
        with tracer.start_as_current_span("orchestrator.process_command") as span:
            span.set_attribute("task_id", task_id)
            
            # 1. Проверка через Policy-as-Code (YAML)
            policy_result = self.policy_engine.check(command)
            if not policy_result.allowed:
                self.state_manager.save_state(TaskState(task_id=task_id, status="blocked_policy", payload=policy_result.reason))
                return False
                
            # 2. Проверка через DCG (Деструктивные команды)
            dcg_result = self.dcg_guard.check_command(command)
            if not dcg_result.allowed:
                self.state_manager.save_state(TaskState(task_id=task_id, status="blocked_dcg", payload=dcg_result.reason))
                return False
                
            # 3. Если всё чисто — разрешаем выполнение
            self.state_manager.save_state(TaskState(task_id=task_id, status="approved", payload=command))
            return True
