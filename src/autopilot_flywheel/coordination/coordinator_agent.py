import json
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.observability.tracer import tracer

class CoordinatorAgent:
    def __init__(self, mail_client: AgentMailClient = None):
        self.mail_client = mail_client or AgentMailClient()

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
                    # ИСПРАВЛЕНО: используем ключ 'from' вместо 'sender_name'
                    sender = msg.get("from", "Unknown")
                    subject = msg.get("subject", "No Subject")
                    print(f"📬 Received: {subject} (from {sender})")
            except json.JSONDecodeError:
                print(f"Failed to parse inbox: {raw_messages}")
