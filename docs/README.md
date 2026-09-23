# 📚 Autopilot Flywheel Documentation

Это навигационная страница по документации проекта.

## Start here

| Документ | Назначение |
|---|---|
| [VISION.md](VISION.md) | Что строим и зачем |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Как система должна быть устроена |
| [INTERFACES.md](INTERFACES.md) | Какие внешние capabilities рассматриваются и что реально verified |
| [VERIFICATION.md](VERIFICATION.md) | Как проверять API/CLI/MCP/contracts |
| [ROADMAP.md](ROADMAP.md) | В каком порядке это реализуется |
| [adr/](adr/) | Почему принимаются значимые архитектурные решения |

## Порядок чтения

Для нового участника:

```text
VISION
  ↓
ARCHITECTURE
  ↓
INTERFACES
  ↓
VERIFICATION
  ↓
ROADMAP
  ↓
ADR
```

Для coding agent дополнительно обязателен корневой [AGENTS.md](../AGENTS.md).

## Source-of-truth map

| Вопрос | Источник |
|---|---|
| Какова цель продукта? | `VISION.md` |
| Каковы системные границы и invariants? | `ARCHITECTURE.md` |
| Подтверждён ли конкретный upstream API? | `INTERFACES.md` |
| Как доказать совместимость? | `VERIFICATION.md` |
| Что делать следующим? | `ROADMAP.md` |
| Почему было принято архитектурное решение? | `adr/` |
| Как должен вести себя AI coding agent? | `../AGENTS.md` |

## Статусы внешних контрактов

- 🟡 **PROPOSED** — capability нужна, интерфейс ещё не подтверждён.
- 🟢 **VERIFIED** — интерфейс подтверждён evidence на конкретной версии.
- 🔵 **IMPLEMENTED** — adapter реализован и покрыт contract/integration tests.
- ⚫ **DEPRECATED** — контракт больше не используется.
- 🔴 **UNKNOWN** — данных недостаточно.

Если documentation и фактическое поведение upstream расходятся, сначала обновляется evidence и `INTERFACES.md`, затем implementation.
