import pytest
import os
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState

@pytest.fixture
def temp_db(tmp_path):
    # Используем временную папку для тестовой БД, чтобы не засорять проект
    db_path = os.path.join(tmp_path, "test_state.db")
    return StateManager(db_path=db_path)

def test_save_and_get_state(temp_db):
    state = TaskState(task_id="task-1", status="in_progress", payload="Step 1 done")
    temp_db.save_state(state)
    
    retrieved = temp_db.get_state("task-1")
    assert retrieved is not None
    assert retrieved.status == "in_progress"
    assert retrieved.payload == "Step 1 done"

def test_update_state(temp_db):
    temp_db.save_state(TaskState(task_id="task-1", status="in_progress"))
    temp_db.save_state(TaskState(task_id="task-1", status="completed"))
    
    retrieved = temp_db.get_state("task-1")
    assert retrieved.status == "completed"

def test_get_missing_state(temp_db):
    assert temp_db.get_state("unknown-task") is None
