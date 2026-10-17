from autopilot_flywheel.prompts.task_models import TaskGraph
from autopilot_flywheel.prompts.llm_client import LLMClient
from autopilot_flywheel.prompts.planner import SYSTEM_PROMPT # Импортируем наш промпт
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState
from autopilot_flywheel.observability.tracer import tracer

class PlannerAgent:
    def __init__(self, llm_client: LLMClient = None):
        self.state_manager = StateManager()
        self.llm_client = llm_client or LLMClient()

    def plan(self, user_request: str) -> TaskGraph:
        with tracer.start_as_current_span("planner.plan") as span:
            span.set_attribute("user_request", user_request)
            
            # Реальный вызов LLM
            raw_response = self.llm_client.generate(
                prompt=user_request,
                system_prompt=SYSTEM_PROMPT
            )
            
            # Очистка ответа от возможных markdown-оберток (```json ... ```)
            clean_json = raw_response.strip().removeprefix("```json").removesuffix("```").strip()
            
            try:
                task_graph = TaskGraph.model_validate_json(clean_json)
            except Exception as e:
                span.record_exception(e)
                raise ValueError(f"LLM returned invalid JSON: {raw_response}")
            
            for task in task_graph.tasks:
                state = TaskState(
                    task_id=task.id, 
                    status="pending", 
                    payload=task.model_dump_json()
                )
                self.state_manager.save_state(state)
                
            span.set_attribute("tasks_created", len(task_graph.tasks))
            return task_graph
