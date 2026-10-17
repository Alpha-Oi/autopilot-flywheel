import yaml
from pydantic import BaseModel
from autopilot_flywheel.observability.tracer import tracer

class PolicyResult(BaseModel):
    command: str
    allowed: bool
    reason: str | None = None

class PolicyEngine:
    def __init__(self, config_path: str = "config/policies.yaml"):
        self.rules = []
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data and "rules" in data:
                    self.rules = data["rules"]
        except FileNotFoundError:
            pass # Если файла нет, разрешаем всё

    def check(self, command: str) -> PolicyResult:
        with tracer.start_as_current_span("policy.check") as span:
            span.set_attribute("command", command)
            
            for rule in self.rules:
                if rule["type"] == "command_contains":
                    if rule["value"] in command:
                        reason = f"Blocked by policy: {rule['name']}"
                        span.set_attribute("allowed", False)
                        return PolicyResult(command=command, allowed=False, reason=reason)
            
            span.set_attribute("allowed", True)
            return PolicyResult(command=command, allowed=True)
