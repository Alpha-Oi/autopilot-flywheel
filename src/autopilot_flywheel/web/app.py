from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.state.models import TaskState
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.prompts.planner_agent import PlannerAgent
from autopilot_flywheel.workers.worker_agent import WorkerAgent
from autopilot_flywheel.coordination.coordinator_agent import CoordinatorAgent
from autopilot_flywheel.reviewer.agent import ReviewerAgent
from autopilot_flywheel.prompts.task_models import TaskNode

app = FastAPI(title="Autopilot Flywheel Dashboard")
templates = Jinja2Templates(directory="src/autopilot_flywheel/web/templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    manager = StateManager()
    raw_tasks = manager.get_all_tasks()
    
    mermaid_lines = ["graph TD"]
    tasks = []
    for t in raw_tasks:
        node = TaskNode.model_validate_json(t.payload)
        safe_id = t.task_id.replace("-", "_")
        mermaid_lines.append(f'    {safe_id}["{t.task_id}<br>{t.status}"]')
        for block in node.blocks:
            safe_block = block.replace("-", "_")
            mermaid_lines.append(f'    {safe_block} --> {safe_id}')
        tasks.append({
            "id": t.task_id,
            "description": node.description,
            "status": t.status,
            "blocks": node.blocks
        })
    mermaid_code = "\n".join(mermaid_lines)
    
    messages = []
    try:
        mail = AgentMailClient()
        raw_msgs = mail.fetch_inbox("default", "Coordinator")
        messages = json.loads(raw_msgs)
    except Exception as e:
        messages = [{"subject": f"Ошибка: {e}", "from": "System"}]

    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"tasks": tasks, "messages": messages, "mermaid_code": mermaid_code}
    )

@app.post("/run-plan")
def run_plan(request: Request, command: str = Form(...)):
    PlannerAgent().plan(command)
    return RedirectResponse(url="/", status_code=303)

@app.post("/run-execute")
def run_execute():
    WorkerAgent().run()
    return RedirectResponse(url="/", status_code=303)

@app.post("/run-coordinate")
def run_coordinate():
    CoordinatorAgent().run()
    return RedirectResponse(url="/", status_code=303)

@app.post("/run-review")
def run_review():
    ReviewerAgent().run()
    return RedirectResponse(url="/", status_code=303)

@app.post("/approve/{task_id}")
def approve_task(task_id: str):
    manager = StateManager()
    state = manager.get_state(task_id)
    if state and state.status == "pending_approval":
        # Меняем статус на human_approved
        new_state = TaskState(task_id=task_id, status="human_approved", payload=state.payload)
        manager.save_state(new_state)
    return RedirectResponse(url="/", status_code=303)
