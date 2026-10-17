import json
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState
from autopilot_flywheel.prompts.task_models import TaskNode
from autopilot_flywheel.observability.tracer import tracer

class CoordinatorAgent:
    def __init__(self, mail_client: AgentMailClient = None, state_manager: StateManager = None):
        self.mail_client = mail_client or AgentMailClient()
        self.state_manager = state_manager or StateManager()

    def run(self, coordinator_id: str = "Coordinator", project: str = "default"):
        with tracer.start_as_current_span("coordinator.run"):
            print(f"👀 Checking inbox for {coordinator_id}...")
            raw_messages = self.mail_client.fetch_inbox(project, coordinator_id)
            
            try:
                messages = json.loads(raw_messages)
                if not messages:
                    print("📭 Inbox is empty.")
                    return
                
                for msg in messages:
                    sender = msg.get("from", "Unknown")
                    subject = msg.get("subject", "No Subject")
                    
                    print(f"📬 Received: {subject} (from {sender})")
                    
                    # Логика: если задача завершена, создаем задачу на написание тестов
                    if subject.startswith("Task ") and subject.endswith(" completed"):
                        # Извлекаем ID задачи (например, из "Task task-1 completed" получаем "task-1")
                        parts = subject.split(" ")
                        if len(parts) >= 3:
                            original_task_id = parts[1]
                            followup_id = f"{original_task_id}-tests"
                            
                            # Проверяем, не создавали ли мы уже такую задачу
                            existing = self.state_manager.get_state(followup_id)
                            if not existing:
                                new_task = TaskNode(
                                    id=followup_id,
                                    description=f"Write tests for {original_task_id}",
                                    blocks=[]
                                )
                                state = TaskState(
                                    task_id=followup_id,
                                    status="pending",
                                    payload=new_task.model_dump_json()
                                )
                                self.state_manager.save_state(state)
                                print(f"✨ Created new follow-up task: {followup_id}")
                            else:
                                print(f"ℹ️ Follow-up task {followup_id} already exists. Skipping.")
                        
            except json.JSONDecodeError:
                print(f"Failed to parse inbox: {raw_messages}")
