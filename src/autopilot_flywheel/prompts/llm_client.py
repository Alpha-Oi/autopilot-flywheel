import os
import litellm
from dotenv import load_dotenv
from autopilot_flywheel.observability.tracer import tracer

# Загружаем переменные окружения из .env (если файл есть)
load_dotenv()

class LLMClient:
    def __init__(self, model: str = None):
        # Если модель не передана, берем из .env или используем дефолтную
        self.model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        with tracer.start_as_current_span("llm.generate") as span:
            span.set_attribute("model", self.model)
            span.set_attribute("prompt_length", len(prompt))
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            try:
                response = litellm.completion(
                    model=self.model,
                    messages=messages,
                    temperature=0.0
                )
                content = response.choices[0].message.content
                span.set_attribute("response_length", len(content))
                return content
            except Exception as e:
                span.record_exception(e)
                raise RuntimeError(f"LLM call failed: {e}")
