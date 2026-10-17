import subprocess
import shutil

class DcgGuard:
    """Обертка для Destructive Command Guard (DCG)."""

    def __init__(self):
        self.dcg_path = shutil.which("dcg")
        if not self.dcg_path:
            raise RuntimeError("DCG не найден в PATH. Убедитесь, что он установлен.")

    def check_command(self, command: str) -> bool:
        """
        Проверяет команду через DCG.
        Возвращает True, если команда безопасна (ALLOWED).
        Возвращает False, если команда заблокирована (BLOCKED).
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
            return True
        return False
