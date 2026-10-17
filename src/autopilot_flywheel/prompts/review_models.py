from pydantic import BaseModel

class ReviewResult(BaseModel):
    task_id: str
    status: str  # "approved" или "needs_fix"
    comment: str = ""
