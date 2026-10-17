import sqlite3
from .models import TaskState
from autopilot_flywheel.observability.tracer import tracer

class StateManager:
    def __init__(self, db_path: str = "autopilot_state.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    payload TEXT
                )
            """)

    def save_state(self, state: TaskState) -> None:
        with tracer.start_as_current_span("state.save") as span:
            span.set_attribute("task_id", state.task_id)
            span.set_attribute("status", state.status)
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO tasks (task_id, status, payload) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(task_id) DO UPDATE SET 
                    status=excluded.status, payload=excluded.payload
                """, (state.task_id, state.status, state.payload))

    def get_state(self, task_id: str) -> TaskState | None:
        with tracer.start_as_current_span("state.get") as span:
            span.set_attribute("task_id", task_id)
            with sqlite3.connect(self.db_path) as conn:
                row = conn.execute("SELECT task_id, status, payload FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
                if row:
                    return TaskState(task_id=row[0], status=row[1], payload=row[2])
            return None

    def get_all_tasks(self) -> list[TaskState]:
        with tracer.start_as_current_span("state.get_all") as span:
            with sqlite3.connect(self.db_path) as conn:
                rows = conn.execute("SELECT task_id, status, payload FROM tasks").fetchall()
                return [TaskState(task_id=r[0], status=r[1], payload=r[2]) for r in rows]
