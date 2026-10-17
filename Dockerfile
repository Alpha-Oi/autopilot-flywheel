FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
CMD ["python", "-m", "autopilot_flywheel.main"]
