# Autopilot Flywheel — Architecture

**Status:** DESIGN  
**Authority:** архитектурный источник истины после `AGENTS.md`  
**Implementation status:** foundation only; внешние контракты требуют верификации

## 1. Цель архитектуры

Autopilot Flywheel должен превратить workflow одиночного coding agent в управляемую систему, где:

- intent пользователя превращается в проверяемую спецификацию;
- работа представляется графом зависимостей;
- независимые задачи выполняются параллельно;
- агенты координируют ownership;
- опасные действия ограничиваются runtime policy;
- состояние и результаты аудируемы;
- опыт может переиспользоваться без превращения ошибок в постоянные правила;
- внешние инструменты заменяемы через adapters.

## 2. Архитектурные источники

- `docs/VISION.md` — продуктовый intent.
- `docs/ARCHITECTURE.md` — границы и инварианты.
- `docs/INTERFACES.md` — фактические интеграционные контракты.
- `docs/VERIFICATION.md` — как контракт получает статус VERIFIED.
- `docs/ROADMAP.md` — последовательность реализации.
- `docs/adr/*` — почему были приняты значимые решения.

## 3. Логические плоскости

### 3.1 Operator Plane

Отвечает за:

- ввод цели;
- видимость плана и прогресса;
- approvals;
- остановку/возобновление;
- просмотр конфликтов, ошибок и audit trail.

### 3.2 Control Plane

**Autopilot Core** владеет lifecycle задачи:

```text
INTAKE
  -> SPECIFIED
  -> PLANNED
  -> CONTEXTUALIZED
  -> SCHEDULED
  -> EXECUTING
  -> VERIFYING
  -> COMPLETED | FAILED | BLOCKED
  -> LEARNING
```

Core координирует capabilities, но не должен знать внутренние детали конкретного vendor tool.

### 3.3 Planning Plane

Предполагаемые компоненты: Beads Workflow + Beads Viewer.

Ответственность:

- task graph;
- dependencies;
- readiness;
- priority signals;
- critical path;
- task identity.

### 3.4 Execution / Orchestration Plane

Предполагаемый компонент: NTM.

Ответственность:

- lifecycle agent sessions;
- assignment;
- parallelism limits;
- checkpoint/recovery;
- health/state reporting.

### 3.5 Coordination Plane

Предполагаемый компонент: MCP Agent Mail.

Ответственность:

- agent identity;
- message exchange;
- ownership/lease intent;
- conflict detection;
- collaboration audit.

### 3.6 Safety Plane

Предполагаемый компонент: DCG плюс собственные policy gates.

Ответственность:

- блокировка destructive actions;
- allow/deny/approval decision;
- policy evidence;
- safe alternatives;
- fail-closed semantics для high-risk operations.

### 3.7 Knowledge Plane

Предполагаемые компоненты: CASS + CASS Memory.

Ответственность:

- индекс сессий;
- retrieval релевантного опыта;
- provenance;
- confidence;
- feedback/outcome;
- promotion/demotion procedural rules.

### 3.8 Deployment Plane

Предполагаемый компонент: ACFS.

Ответственность:

- reproducible environment;
- version pinning;
- preflight;
- install/update/rollback strategy.

## 4. Обязательная adapter boundary

Нормативный принцип:

```text
Autopilot Core
    |
    v
Internal Capability Contract
    |
    v
Adapter
    |
    v
External Tool
```

Core не должен импортировать vendor-specific JSON/CLI/MCP semantics глубже adapter boundary.

Минимальный набор внутренних capability families:

- `Planner`
- `TaskGraphAnalyzer`
- `Orchestrator`
- `Coordinator`
- `SafetyGuard`
- `MemoryProvider`
- `DeploymentProvider`

Конкретные сигнатуры фиксируются позже, после Phase 0.

## 5. Canonical execution flow

```text
1. User intent
2. Spec normalization
3. Task graph creation
4. Graph validation
5. Memory/context retrieval
6. Scheduling
7. Agent registration
8. Ownership/lease acquisition
9. Safety preflight
10. Execution
11. Incremental verification
12. Integration verification
13. Outcome recording
14. Memory feedback/distillation
15. Final operator report
```

Каждый шаг должен иметь correlation/task/run identifiers.

## 6. Data ownership

| Data | Canonical owner | Требование |
|---|---|---|
| User intent / spec | Autopilot Core | versioned, immutable revisions |
| Task graph | Planning capability | stable task IDs |
| Run state | Orchestrator adapter | resumable/checkpointable |
| Coordination messages | Coordinator | auditable |
| File ownership/leases | Coordinator | expiry + conflict semantics |
| Safety decisions | Safety plane | immutable audit event |
| Session index | CASS-like provider | provenance |
| Procedural rules | Memory provider | confidence + provenance |
| Final result | Core | verification evidence |

До выбора physical storage эти ownership rules логические.

## 7. Safety invariants

1. **Fail closed for destructive operations.**
2. Нельзя обходить guard из-за недоступности guard.
3. Approval должен быть связан с конкретным action scope.
4. Workspace boundary должен быть явным.
5. Секреты не должны попадать в shared memory/audit без редактирования.
6. Агент не может сам повысить собственные permissions.
7. Conflict/lease violation переводит работу в BLOCKED или replan, а не в silent overwrite.

## 8. Graceful degradation

Graceful degradation разрешена только если сохраняются safety invariants.

| Отказ | Допустимое поведение |
|---|---|
| Memory unavailable | продолжить без learned context; пометить run degraded |
| Graph analytics unavailable | использовать validated dependency order без advanced ranking |
| Coordinator unavailable при single-agent | возможно продолжение в single-agent mode |
| Coordinator unavailable при multi-agent | остановить parallel writes |
| Safety guard unavailable | запретить high-risk commands; fail closed |
| Orchestrator unavailable | не стартовать новые agents; сохранить plan/state |
| Deployment helper unavailable | ручной documented setup; не угадывать installer |

## 9. Idempotency and recovery

Каждая операция должна стремиться к модели:

```text
request_id + desired_state -> observable result
```

Повторный вызов не должен:

- создавать дубликаты task;
- повторно применять уже применённый patch;
- захватывать тот же lease как новый;
- дважды записывать один outcome;
- терять связь с исходным run.

Нужны checkpoints на границах стадий lifecycle.

## 10. Audit model

Минимальное событие:

```text
AuditEvent
- event_id
- timestamp
- correlation_id
- run_id
- task_id?
- agent_id?
- capability
- action
- decision/status
- evidence_ref?
- parent_event_id?
```

Физический формат пока PROPOSED.

## 11. Non-goals текущей фазы

Сейчас проект не фиксирует:

- язык реализации Core;
- базу данных;
- конкретный transport между всеми слоями;
- реальные ports;
- production auth model;
- окончательный UI;
- точные внешние command names;
- обязательность конкретного upstream tool навсегда.

## 12. Архитектурные gates

### Gate A — Verified Interfaces
Нельзя переходить к integration implementation до подтверждения external capabilities.

### Gate B — Safety Vertical Slice
Первый end-to-end slice обязан включать safety, audit и rollback semantics.

### Gate C — Single Agent Before Multi-Agent
Сначала deterministic single-agent lifecycle, затем parallel execution.

### Gate D — Memory After Verification
Memory не должна влиять на решения до появления provenance, feedback и invalidation path.

## 13. Требующие ADR решения

- runtime языка/процесса Core;
- persistence layer;
- event model;
- adapter protocol;
- policy engine;
- orchestrator;
- memory promotion algorithm;
- deployment topology;
- stable public API.

Шаблон: `docs/adr/0000-template.md`.
