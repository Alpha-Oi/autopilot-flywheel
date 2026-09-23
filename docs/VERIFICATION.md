# Autopilot Flywheel — Integration Verification Protocol

**Purpose:** не допустить, чтобы архитектура строилась на устаревших, выдуманных или несовместимых API.

## 1. Когда запускать

Обязательно:

- после стабилизации `autopilot-jet`;
- перед первой реализацией каждого adapter;
- перед major upgrade upstream dependency;
- если upstream изменил CLI/MCP/API;
- если contract test начал расходиться с реальным поведением.

## 2. Что считается evidence

Сильное evidence:

1. фактический код/схема upstream на pinned commit;
2. official docs того же релиза;
3. `--help` / schema / capability discovery из реально установленной версии;
4. machine-readable OpenAPI/MCP schema, если существует;
5. воспроизводимый smoke test.

Слабое evidence:

- блог;
- screenshot;
- старый issue;
- сообщение модели;
- память из предыдущей сессии;
- пример без версии.

Слабое evidence может направить исследование, но не переводит контракт в VERIFIED.

## 3. Verification checklist для каждого инструмента

### Identity

- [ ] Repository подтверждён
- [ ] License проверена
- [ ] Version/tag записан
- [ ] Commit SHA записан
- [ ] Последняя проверка датирована

### Installation

- [ ] Поддерживаемая OS
- [ ] Runtime prerequisites
- [ ] Package/install method
- [ ] Idempotent install/update path
- [ ] Uninstall/rollback path

### Capability surface

- [ ] Реальные команды/подкоманды
- [ ] Реальные MCP tools/resources
- [ ] Реальные REST/OpenAPI routes
- [ ] Input schema
- [ ] Output schema
- [ ] Error behavior
- [ ] Exit codes
- [ ] Timeout/cancellation
- [ ] Streaming/event semantics

### State and concurrency

- [ ] Где хранится состояние
- [ ] Что persistent
- [ ] Что process-local
- [ ] Lock/lease semantics
- [ ] Crash recovery
- [ ] Concurrent writers behavior
- [ ] Idempotency guarantees

### Security

- [ ] Auth
- [ ] Secret handling
- [ ] Privilege requirements
- [ ] Dangerous commands/actions
- [ ] Network exposure
- [ ] Default bind address
- [ ] Auditability
- [ ] Failure mode

### Compatibility

- [ ] Windows
- [ ] Linux
- [ ] WSL/container/VPS при необходимости
- [ ] Claude Code
- [ ] Codex
- [ ] Gemini/other target agents
- [ ] Known conflicts

## 4. Evidence record

На каждую интеграцию создаётся запись в PR/issue или отдельный файл evidence:

```text
Integration:
Repository:
Version:
Commit SHA:
Verified date:
Verifier:
Environment:

Observed capabilities:
Observed commands/tools:
Observed schemas:
Observed failures:
Security notes:
Compatibility notes:

Evidence links/files:
- ...

Conclusion:
- VERIFIED | NOT VERIFIED | PARTIALLY VERIFIED
```

## 5. Минимальный smoke test

Smoke test не должен менять пользовательские данные.

Порядок:

1. version/capability discovery;
2. no-op/read-only call;
3. deterministic local fixture;
4. invalid-input test;
5. timeout/cancel test;
6. restart/recovery test, если stateful;
7. concurrency test, если используется параллельно;
8. security-deny test, если safety-sensitive.

## 6. Критерий VERIFIED

Статус VERIFIED допустим, когда:

- версия pinned;
- capability реально вызвана;
- inputs/outputs наблюдались;
- ошибка наблюдалась хотя бы на invalid request;
- security implications описаны;
- evidence доступно reviewer;
- ограничения записаны в `INTERFACES.md`.

## 7. Phase 0 matrix

| Integration | Identity | Interface | State | Security | Compatibility | Status |
|---|---:|---:|---:|---:|---:|---|
| Beads Workflow | ☐ | ☐ | ☐ | ☐ | ☐ | PROPOSED |
| Beads Viewer | ☐ | ☐ | ☐ | ☐ | ☐ | PROPOSED |
| NTM | ☐ | ☐ | ☐ | ☐ | ☐ | PROPOSED |
| MCP Agent Mail | ☐ | ☐ | ☐ | ☐ | ☐ | PROPOSED |
| DCG | ☐ | ☐ | ☐ | ☐ | ☐ | PROPOSED |
| CASS | ☐ | ☐ | ☐ | ☐ | ☐ | PROPOSED |
| CASS Memory | ☐ | ☐ | ☐ | ☐ | ☐ | PROPOSED |
| ACFS | ☐ | ☐ | ☐ | ☐ | ☐ | PROPOSED |

## 8. Правило отрицательного результата

Если предположение из Vision не подтверждается, **мы меняем архитектуру, а не подгоняем evidence под Vision**.

Неподтверждённая интеграция должна:

- остаться PROPOSED/UNKNOWN;
- получить alternative candidate;
- при необходимости породить ADR;
- не блокировать исследование остальных слоёв.
