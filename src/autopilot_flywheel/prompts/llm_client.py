import os
import litellm
from dotenv import load_dotenv
from autopilot_flywheel.observability.tracer import tracer

load_dotenv()

class LLMClient:
    def __init__(self, model: str = None):
        self.model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        with tracer.start_as_current_span("llm.generate") as span:
            span.set_attribute("model", self.model)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            api_key = os.getenv("OPENAI_API_KEY", "")
            kwargs = {"temperature": 0.0}
            
            if not api_key or "your-key" in api_key:
                span.set_attribute("mock_mode", True)
                # ИСПРАВЛЕНО: используем одинарные кавычки внутри команды
                kwargs["mock_response"] = """
                {
                  "tasks": [
                    {"id": "task-1", "description": "Create API directory", "blocks": [], "command": "mkdir api"},
                    {"id": "task-2", "description": "Create auth file", "blocks": ["task-1"], "command": "echo '# Auth Module' > api/auth.py"}
                  ]
                }
                """
            else:
                span.set_attribute("mock_mode", False)

            try:
                response = litellm.completion(
                    model=self.model,
                    messages=messages,
                    **kwargs
                )
                return response.choices[0].message.content
            except Exception as e:
                span.record_exception(e)
                raise RuntimeError(f"LLM call failed: {e}")
