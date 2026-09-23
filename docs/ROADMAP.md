# Autopilot Flywheel — Roadmap

Roadmap построен через **gates**, а не только через список функций. Переход к следующей фазе требует evidence.

## Phase 0 — Foundation & Verification

### Цель
Зафиксировать intent, архитектуру и реальные интеграционные контракты до production-кода.

### Deliverables
- [x] Detailed Vision
- [x] Architecture foundation
- [x] Integration registry
- [x] Verification protocol
- [x] Agent governance rules
- [x] ADR process
- [ ] `autopilot-jet` stable baseline identified
- [ ] baseline version/commit pinned
- [ ] все candidate integrations проверены
- [ ] compatibility matrix заполнена
- [ ] минимальный vertical slice выбран

### Exit criteria
- нет внешнего REQUIRED контракта со статусом UNKNOWN;
- для REQUIRED интеграций есть pinned evidence;
- safety policy не зависит от best-effort поведения;
- создан ADR для runtime/persistence решений, если они уже выбираются.

---

## Phase 1 — Core Contracts & Safety Skeleton

### Цель
Создать внутренние capability contracts и безопасный single-agent lifecycle.

### Deliverables
- [ ] Core lifecycle state machine
- [ ] adapter interfaces
- [ ] normalized error taxonomy
- [ ] audit event model
- [ ] correlation/run/task IDs
- [ ] safety decision boundary
- [ ] workspace scope policy
- [ ] destructive-action negative tests

### Exit criteria
Single-agent task может пройти intent → execute → verify с audit trail, при этом destructive path блокируется.

---

## Phase 2 — Memory (CASS + CASS Memory candidate)

### Цель
Добавить retrieval и outcome feedback без неконтролируемого "самообучения".

### Deliverables
- [ ] session indexing adapter
- [ ] memory query adapter
- [ ] provenance
- [ ] confidence
- [ ] feedback/outcome
- [ ] invalidation/supersession
- [ ] memory-off mode

### Exit criteria
Memory improves context but её отключение не ломает базовый lifecycle.

---

## Phase 3 — Planning Graph

### Цель
Перейти от линейного списка к dependency-aware task graph.

### Deliverables
- [ ] spec → task graph
- [ ] graph validation
- [ ] ready/blocked states
- [ ] prioritization adapter
- [ ] critical-path signal
- [ ] graph visualization feed

### Exit criteria
System не запускает blocked task и детерминированно объясняет, почему task ready/blocked.

---

## Phase 4 — Orchestration

### Цель
Ввести управляемый runtime agents.

### Deliverables
- [ ] session spawn/stop adapter
- [ ] health
- [ ] cancellation
- [ ] checkpoint
- [ ] recovery
- [ ] concurrency limits
- [ ] operator pause/resume

### Exit criteria
Single-agent и controlled multi-session execution переживают restart без потери task identity.

---

## Phase 5 — Multi-Agent Coordination

### Цель
Разрешить параллельные изменения без silent overwrite.

### Deliverables
- [ ] agent identity
- [ ] messaging
- [ ] ownership/leases
- [ ] conflict detection
- [ ] pre-write/pre-commit enforcement
- [ ] stale lease recovery
- [ ] 5+ agent stress test

### Exit criteria
Параллельные agents не могут молча перезаписать один mutable scope.

---

## Phase 6 — Deployment & Reproducibility

### Цель
Воспроизводимая установка и recovery.

### Deliverables
- [ ] environment manifest
- [ ] pinned versions
- [ ] preflight
- [ ] one-command candidate setup
- [ ] update strategy
- [ ] rollback strategy
- [ ] clean VPS benchmark
- [ ] local/container development path

### Exit criteria
Чистая поддерживаемая среда достигает одинакового verified baseline воспроизводимо.

---

## Phase 7 — Productization

### Deliverables
- [ ] operator dashboard
- [ ] onboarding
- [ ] example projects
- [ ] benchmarks
- [ ] failure/recovery UX
- [ ] security review
- [ ] documentation set
- [ ] v1.0 release criteria

## Metrics

Метрики из Vision считаются **targets**, пока не появится benchmark protocol.

До публикации сравнений необходимо определить:

- benchmark corpus;
- model versions;
- token/cost budget;
- wall-clock methodology;
- pass/fail quality criteria;
- number of runs;
- variance;
- failure handling.

Нельзя заявлять "3–5x faster" как достигнутый результат до измерения по этому протоколу.
