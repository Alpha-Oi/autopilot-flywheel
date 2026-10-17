from pydantic import BaseModel
from typing import List, Optional

class TaskNode(BaseModel):
    id: str
    description: str
    blocks: List[str] = []
    command: Optional[str] = None  # Новая команда для выполнения

class TaskGraph(BaseModel):
    tasks: List[TaskNode]
