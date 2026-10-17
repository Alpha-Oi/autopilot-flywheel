from autopilot_flywheel.prompts.task_models import TaskGraph
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState
from autopilot_flywheel.observability.tracer import tracer

class PlannerAgent:
    def __init__(self):
        self.state_manager = StateManager()

    def plan(self, user_request: str) -> TaskGraph:
        """
        Имитация вызова LLM. В будущем здесь будет реальный API-запрос.
        """
        with tracer.start_as_current_span("planner.plan") as span:
            span.set_attribute("user_request", user_request)
            
            # ЗАГЛУШКА: Представим, что LLM вернула такой JSON
            mock_llm_response = """
            {
              "tasks": [
                {"id": "task-1", "description": "Create API skeleton", "blocks": []},
                {"id": "task-2", "description": "Implement auth", "blocks": ["task-1"]}
              ]
            }
            """
            
            # Валидация ответа через Pydantic
            task_graph = TaskGraph.model_validate_json(mock_llm_response)
            
            # Сохраняем задачи в БД
            for task in task_graph.tasks:
                state = TaskState(
                    task_id=task.id, 
                    status="pending", 
                    payload=task.description
                )
                self.state_manager.save_state(state)
                
            span.set_attribute("tasks_created", len(task_graph.tasks))
            return task_graph
