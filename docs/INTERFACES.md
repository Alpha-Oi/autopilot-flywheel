# Autopilot Flywheel — Integration Interfaces Registry

**Status:** DESIGN / VERIFICATION REQUIRED

Этот документ — реестр внешних интеграций. Он специально отделяет **намерение** от **подтверждённого контракта**.

## 1. Статусы

- **PROPOSED** — capability нужна архитектуре, но фактический интерфейс не подтверждён.
- **VERIFIED** — интерфейс проверен по конкретной версии/commit SHA и evidence сохранено.
- **IMPLEMENTED** — adapter реализован и покрыт contract/integration tests.
- **DEPRECATED** — контракт больше не должен использоваться.
- **UNKNOWN** — данных недостаточно даже для устойчивой гипотезы.

Только VERIFIED/IMPLEMENTED может использоваться как фактический внешний контракт.

## 2. Реестр

| Capability | Candidate upstream | Status | Pinned version/SHA | Evidence | Adapter |
|---|---|---:|---|---|---|
| Planning transform | Dicklesworthstone/beads-workflow | PROPOSED | — | — | — |
| Graph analysis | Dicklesworthstone/beads_viewer | PROPOSED | — | — | — |
| Agent orchestration | Dicklesworthstone/named_tmux_manager | PROPOSED | — | — | — |
| Coordination / leases | Dicklesworthstone/mcp_agent_mail | PROPOSED | — | — | — |
| Destructive command guard | Dicklesworthstone/destructive_command_guard | PROPOSED | — | — | — |
| Session search | Dicklesworthstone/coding_agent_session_search | PROPOSED | — | — | — |
| Procedural memory | Dicklesworthstone/cass_memory_system | PROPOSED | — | — | — |
| Environment setup | Dicklesworthstone/agentic_coding_flywheel_setup | PROPOSED | — | — | — |

## 3. Важное правило

Ранние документы содержали примеры вроде:

- `bv --robot-triage`;
- `ntm spawn ...`;
- `cm context ...`;
- `cm outcome ...`;
- предполагаемые MCP inbox/outbox/file leases;
- `dcg scan ...`;
- предполагаемые localhost endpoints.

**Они являются design hypotheses, а не подтверждёнными контрактами.**

Не реализовывать production integration против этих примеров, пока соответствующая строка реестра не станет VERIFIED.

## 4. Что требуется для VERIFIED

Для каждого upstream:

```text
Repository:
Version/tag:
Commit SHA:
Verified at:
Official README/docs refs:
Executable/package version:
Supported platform:
Transport:
Auth requirements:
Capability surface:
Inputs:
Outputs:
Errors:
Streaming semantics:
Concurrency semantics:
Persistence semantics:
Security notes:
License:
Evidence artifacts:
Known incompatibilities:
```

## 5. Внутренние контракты

Ниже — **наши** proposed abstractions. Они не утверждают форму upstream API.

### 5.1 TaskDescriptor

```text
TaskDescriptor
- task_id
- parent_id?
- title
- objective
- dependencies[]
- acceptance_criteria[]
- risk_level
- preferred_capabilities[]
- state
```

### 5.2 AgentRun

```text
AgentRun
- run_id
- task_id
- agent_id
- model/provider?
- started_at
- checkpoint_ref?
- state
- result_ref?
```

### 5.3 CoordinationLease

```text
CoordinationLease
- lease_id
- owner_agent_id
- resource_scope
- acquired_at
- expires_at
- mode
- state
```

### 5.4 MemoryContext

```text
MemoryContext
- query_id
- items[]
  - content
  - provenance
  - confidence
  - scope
  - created_at
  - supersedes?
```

### 5.5 OutcomeRecord

```text
OutcomeRecord
- outcome_id
- task_id
- run_id
- status
- verification_refs[]
- lessons[]
- confidence
```

### 5.6 SafetyDecision

```text
SafetyDecision
- decision_id
- action_fingerprint
- classification
- policy
- result: allow | deny | require_approval
- rationale
- approval_ref?
```

Эти структуры могут изменяться через ADR до implementation freeze.

## 6. Adapter contract policy

Любой adapter должен:

1. объявлять `adapter_version`;
2. уметь сообщить detected upstream version;
3. иметь capability discovery или явный compatibility matrix;
4. нормализовать ошибки;
5. не протекать vendor-specific типами в Core;
6. иметь timeout/cancellation semantics;
7. иметь health/preflight;
8. иметь deterministic test fixtures для contract tests.

## 7. Error taxonomy

Внутренний слой должен различать минимум:

- `UNAVAILABLE`
- `UNSUPPORTED_VERSION`
- `INVALID_REQUEST`
- `AUTH_REQUIRED`
- `CONFLICT`
- `TIMEOUT`
- `POLICY_DENIED`
- `UPSTREAM_FAILURE`
- `CORRUPT_STATE`

Raw upstream error сохраняется как evidence/debug metadata, но не становится core-domain API.

## 8. Versioning

Не использовать `latest` как production contract.

Для каждой интеграции:

- pin version/commit;
- определить минимальную/максимальную совместимость;
- проверить upgrade отдельно;
- зафиксировать breaking changes;
- обновить evidence date.

## 9. Verification → implementation flow

```text
PROPOSED
   |
   v
collect evidence
   |
   v
VERIFIED
   |
   v
write adapter + contract tests
   |
   v
IMPLEMENTED
   |
   v
runtime compatibility check
```

Полная процедура: [VERIFICATION.md](VERIFICATION.md).
