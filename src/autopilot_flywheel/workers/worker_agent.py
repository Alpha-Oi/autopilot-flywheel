import subprocess
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState
from autopilot_flywheel.prompts.task_models import TaskNode
from autopilot_flywheel.observability.tracer import tracer
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.coordination.models import AgentMessage
from autopilot_flywheel.orchestrator import AutopilotOrchestrator

class WorkerAgent:
    def __init__(self, mail_client: AgentMailClient = None):
        self.state_manager = StateManager()
        self.mail_client = mail_client or AgentMailClient()
        self.orchestrator = AutopilotOrchestrator()

    def run(self, coordinator_id: str = "Coordinator"):
        with tracer.start_as_current_span("worker.run"):
            tasks = self.state_manager.get_all_tasks()
            statuses = {t.task_id: t.status for t in tasks}
            
            for task_state in tasks:
                # Воркер берет задачи в статусе pending или human_approved
                if task_state.status not in ["pending", "human_approved"]:
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
            
            if node.command:
                print(f"  > Running command: {node.command}")
                
                # Если статус human_approved, мы пропускаем проверку
                if state.status == "human_approved":
                    print("  ✅ Approved by human. Bypassing security checks.")
                    allowed = True
                else:
                    allowed = self.orchestrator.process_command(task_id=node.id, command=node.command)
                
                if not allowed:
                    print(f"⚠️ Task {node.id} blocked! Waiting for human approval.")
                    new_state = TaskState(task_id=node.id, status="pending_approval", payload=state.payload)
                    self.state_manager.save_state(new_state)
                    return

                try:
                    result = subprocess.run(node.command, shell=True, capture_output=True, text=True, cwd=".")
                    if result.returncode == 0:
                        print(f"  ✅ Command output: {result.stdout.strip()}")
                    else:
                        print(f"  ❌ Command failed: {result.stderr.strip()}")
                except Exception as e:
                    print(f"  ❌ Execution error: {e}")

            new_state = TaskState(task_id=node.id, status="completed", payload=state.payload)
            self.state_manager.save_state(new_state)
            print(f"✅ Task {node.id} completed.")
            
            msg = AgentMessage(
                project="default",
                sender="WorkerAgent",
                recipient=coordinator_id,
                subject=f"Task {node.id} completed",
                body=f"Task {node.id} ({node.description}) has been completed."
            )
            self.mail_client.send_message_nowait(msg)
            print(f"📨 Notification dispatched to {coordinator_id}.")
