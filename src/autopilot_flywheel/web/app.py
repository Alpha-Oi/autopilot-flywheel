from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.coordination.agent_mail import AgentMailClient
from autopilot_flywheel.prompts.planner_agent import PlannerAgent
from autopilot_flywheel.workers.worker_agent import WorkerAgent
from autopilot_flywheel.coordination.coordinator_agent import CoordinatorAgent
from autopilot_flywheel.reviewer.agent import ReviewerAgent

app = FastAPI(title="Autopilot Flywheel Dashboard")
templates = Jinja2Templates(directory="src/autopilot_flywheel/web/templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    manager = StateManager()
    tasks = manager.get_all_tasks()
    messages = []
    try:
        mail = AgentMailClient()
        raw_msgs = mail.fetch_inbox("default", "Coordinator")
        messages = json.loads(raw_msgs)
    except Exception as e:
        messages = [{"subject": f"Ошибка: {e}", "from": "System"}]

    return templates.TemplateResponse(
        request=request, name="index.html", context={"tasks": tasks, "messages": messages}
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
