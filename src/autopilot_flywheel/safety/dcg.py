import subprocess
import shutil
from pydantic import BaseModel
from autopilot_flywheel.observability.tracer import tracer

class DcgResult(BaseModel):
    command: str
    allowed: bool
    reason: str | None = None

class DcgGuard:
    def __init__(self):
        self.dcg_path = shutil.which("dcg")
        if not self.dcg_path:
            raise RuntimeError("DCG не найден в PATH.")

    def check_command(self, command: str) -> DcgResult:
        with tracer.start_as_current_span("dcg.check_command") as span:
            span.set_attribute("command", command)
            
            try:
                result = subprocess.run(
                    [self.dcg_path, "test", command],
                    capture_output=True, text=True, encoding="utf-8", errors="ignore"
                )
                allowed = "Result: ALLOWED" in result.stdout or result.returncode == 0
            except (ValueError, OSError) as e:
                # Если команда содержит нулевые байты или другие спецсимволы
                allowed = False
                span.record_exception(e)
                
            span.set_attribute("allowed", allowed)
            if allowed:
                return DcgResult(command=command, allowed=True)
            return DcgResult(command=command, allowed=False, reason="Blocked by DCG or invalid input")
