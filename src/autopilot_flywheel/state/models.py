from pydantic import BaseModel

class TaskState(BaseModel):
    task_id: str
    status: str
    payload: str = ""
