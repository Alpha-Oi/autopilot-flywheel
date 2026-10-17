from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from autopilot_flywheel.state.manager import StateManager
from autopilot_flywheel.coordination.agent_mail import AgentMailClient

app = FastAPI(title="Autopilot Flywheel Dashboard")
templates = Jinja2Templates(directory="src/autopilot_flywheel/web/templates")

# ВАЖНО: убираем async, чтобы FastAPI выполнял функцию в отдельном потоке.
# Это позволит использовать asyncio.run() внутри AgentMailClient.
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    # 1. Получаем задачи из SQLite
    manager = StateManager()
    tasks = manager.get_all_tasks()
    
    # 2. Пытаемся получить письма из Agent Mail
    messages = []
    try:
        mail = AgentMailClient()
        raw_msgs = mail.fetch_inbox("default", "Coordinator")
        messages = json.loads(raw_msgs)
    except Exception as e:
        messages = [{"subject": f"Ошибка подключения: {e}", "from": "System"}]

    # 3. Возвращаем шаблон с правильным порядком аргументов
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"tasks": tasks, "messages": messages}
    )
