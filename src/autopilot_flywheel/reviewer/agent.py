from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState
from autopilot_flywheel.prompts.task_models import TaskNode
from autopilot_flywheel.observability.tracer import tracer

class ReviewerAgent:
    def __init__(self):
        self.state_manager = StateManager()

    def run(self):
        with tracer.start_as_current_span("reviewer.run"):
            tasks = self.state_manager.get_all_tasks()
            
            for task_state in tasks:
                if task_state.status != "completed":
                    continue
                
                task_node = TaskNode.model_validate_json(task_state.payload)
                
                # Простая логика ревью: если в описании есть "auth", требуем исправления
                if "auth" in task_node.description.lower():
                    print(f"🔍 Reviewing {task_node.id}: Needs security fix!")
                    # Меняем статус на "needs_fix"
                    new_state = TaskState(task_id=task_node.id, status="needs_fix", payload=task_state.payload)
                    self.state_manager.save_state(new_state)
                    
                    # Создаем задачу на исправление
                    fix_id = f"{task_node.id}-fix"
                    if not self.state_manager.get_state(fix_id):
                        fix_task = TaskNode(
                            id=fix_id,
                            description=f"Fix security issues in {task_node.id}",
                            blocks=[task_node.id]
                        )
                        fix_state = TaskState(task_id=fix_id, status="pending", payload=fix_task.model_dump_json())
                        self.state_manager.save_state(fix_state)
                        print(f"✨ Created fix task: {fix_id}")
                else:
                    print(f"✅ Reviewing {task_node.id}: Approved.")
