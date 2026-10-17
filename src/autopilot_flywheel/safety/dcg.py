import subprocess
import shutil
from pydantic import BaseModel, Field

class DcgResult(BaseModel):
    command: str
    allowed: bool
    reason: str | None = None

class DcgGuard:
    """Обертка для Destructive Command Guard (DCG) с использованием Pydantic."""

    def __init__(self):
        self.dcg_path = shutil.which("dcg")
        if not self.dcg_path:
            raise RuntimeError("DCG не найден в PATH. Убедитесь, что он установлен.")

    def check_command(self, command: str) -> DcgResult:
        """
        Проверяет команду через DCG.
        Возвращает DcgResult с результатом проверки.
        """
        result = subprocess.run(
            [self.dcg_path, "test", command],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        
        # DCG возвращает 0, если команда разрешена, и >0, если заблокирована
        if "Result: ALLOWED" in result.stdout or result.returncode == 0:
            return DcgResult(command=command, allowed=True)
            
        return DcgResult(
            command=command, 
            allowed=False, 
            reason="Blocked by DCG (Destructive Command Guard)"
        )
