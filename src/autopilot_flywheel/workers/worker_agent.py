from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState
from autopilot_flywheel.prompts.task_models import TaskNode
from autopilot_flywheel.observability.tracer import tracer

class WorkerAgent:
    def __init__(self):
        self.state_manager = StateManager()

    def run(self):
        """Запускает цикл выполнения всех доступных задач."""
        with tracer.start_as_current_span("worker.run"):
            tasks = self.state_manager.get_all_tasks()
            
            # Словарь для быстрой проверки статусов
            statuses = {t.task_id: t.status for t in tasks}
            
            for task_state in tasks:
                if task_state.status != "pending":
                    continue
                    
                task_node = TaskNode.model_validate_json(task_state.payload)
                
                # Проверяем зависимости (blocks)
                can_execute = all(statuses.get(b) == "completed" for b in task_node.blocks)
                
                if can_execute:
                    self.execute_task(task_state, task_node)
                    statuses[task_state.task_id] = "completed" # Обновляем локальный статус

    def execute_task(self, state: TaskState, node: TaskNode):
        with tracer.start_as_current_span("worker.execute_task") as span:
            span.set_attribute("task_id", node.id)
            
            # Симуляция работы агента (в реальности здесь был бы вызов LLM/кода)
            print(f"⚙️ Executing: {node.description}...")
            
            # Обновляем статус в БД
            new_state = TaskState(task_id=node.id, status="completed", payload=state.payload)
            self.state_manager.save_state(new_state)
            print(f"✅ Task {node.id} completed.")
