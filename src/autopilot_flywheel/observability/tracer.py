from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Настраиваем провайдер трассировки (пока выводим в консоль для отладки)
provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Создаем глобальный трейсер для проекта
tracer = trace.get_tracer("autopilot_flywheel")
