from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState
from autopilot_flywheel.prompts.task_models import TaskNode
from autopilot_flywheel.observability.tracer import tracer
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.coordination.models import AgentMessage

class WorkerAgent:
    def __init__(self, mail_client: AgentMailClient = None):
        self.state_manager = StateManager()
        self.mail_client = mail_client or AgentMailClient()

    def run(self, coordinator_id: str = "Coordinator"):
        with tracer.start_as_current_span("worker.run"):
            tasks = self.state_manager.get_all_tasks()
            statuses = {t.task_id: t.status for t in tasks}
            
            for task_state in tasks:
                if task_state.status != "pending":
                    continue
                    
                task_node = TaskNode.model_validate_json(task_state.payload)
                can_execute = all(statuses.get(b) == "completed" for b in task_node.blocks)
                
                if can_execute:
                    self.execute_task(task_state, task_node, coordinator_id)
                    statuses[task_state.task_id] = "completed"

    def execute_task(self, state: TaskState, node: TaskNode, coordinator_id: str):
        with tracer.start_as_current_span("worker.execute_task") as span:
            span.set_attribute("task_id", node.id)
            
            print(f"⚙️ Executing: {node.description}...")
            
            new_state = TaskState(task_id=node.id, status="completed", payload=state.payload)
            self.state_manager.save_state(new_state)
            print(f"✅ Task {node.id} completed.")
            
            msg = AgentMessage(
                project="default",
                sender="WorkerAgent",
                recipient=coordinator_id,
                subject=f"Task {node.id} completed",
                body=f"Task {node.id} ({node.description}) has been completed successfully."
            )
            try:
                self.mail_client.send_message(msg)
                print(f"📨 Notification sent to {coordinator_id}.")
            except Exception as e:
                print(f"⚠️ Failed to send notification: {e}")
