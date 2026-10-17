from pydantic import BaseModel
from typing import List

class TaskNode(BaseModel):
    id: str
    description: str
    blocks: List[str] = []

class TaskGraph(BaseModel):
    tasks: List[TaskNode]
