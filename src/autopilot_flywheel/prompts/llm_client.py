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
            span.set_attribute("prompt_length", len(prompt))
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            # Проверяем, есть ли РЕАЛЬНЫЙ ключ, а не заглушка
            api_key = os.getenv("OPENAI_API_KEY", "")
            kwargs = {"temperature": 0.0}
            
            # Если ключа нет или в нем есть "your-key", включаем мок
            if not api_key or "your-key" in api_key:
                span.set_attribute("mock_mode", True)
                kwargs["mock_response"] = """
                {
                  "tasks": [
                    {"id": "task-1", "description": "Create API skeleton", "blocks": []},
                    {"id": "task-2", "description": "Implement auth", "blocks": ["task-1"]}
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
                content = response.choices[0].message.content
                span.set_attribute("response_length", len(content))
                return content
            except Exception as e:
                span.record_exception(e)
                raise RuntimeError(f"LLM call failed: {e}")
