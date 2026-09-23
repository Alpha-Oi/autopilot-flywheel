# Autopilot Flywheel

> Мультиагентная самообучающаяся платформа для автономной разработки ПО.  
> Эволюция [autopilot-jet](https://github.com/Alpha-Oi/autopilot-jet) в сторону безопасной, координируемой и обучающейся агентной фабрики.

![status: vision](https://img.shields.io/badge/status-vision-blue)
![stage: foundation](https://img.shields.io/badge/stage-foundation-orange)
![license: MIT](https://img.shields.io/badge/license-MIT-green)

## Статус проекта

**Текущий режим: DESIGN / FOUNDATION.**

Репозиторий фиксирует архитектуру, границы компонентов, правила для AI-агентов и процедуру верификации интеграций. Полноценная реализация Flywheel не должна начинаться до завершения и стабилизации базового проекта [autopilot-jet](https://github.com/Alpha-Oi/autopilot-jet) и прохождения Phase 0 Verification Gate.

Это ограничение намеренное: внешние CLI, MCP tools, REST endpoints, схемы данных и версии зависимостей должны быть подтверждены по фактическим upstream-репозиториям перед тем, как код начнёт от них зависеть.

## Главные документы

| Документ | Назначение |
|---|---|
| [docs/VISION.md](docs/VISION.md) | Продуктовое видение, мотивация и целевой эффект |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Архитектурные границы, потоки, инварианты и режимы отказа |
| [docs/INTERFACES.md](docs/INTERFACES.md) | Реестр интеграций и правила фиксации внешних контрактов |
| [docs/VERIFICATION.md](docs/VERIFICATION.md) | Процедура проверки upstream API/CLI/MCP и evidence requirements |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Поэтапная реализация и exit criteria |
| [AGENTS.md](AGENTS.md) | Обязательные правила для Codex, Claude Code и других coding agents |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Правила изменений, PR и архитектурных решений |
| [docs/adr/](docs/adr/) | Architecture Decision Records |

## Целевая архитектура

```text
User / Operator
      |
      v
+-------------------------+
|     Autopilot Core      |  <- intent, spec, verification, dashboard
+------------+------------+
             |
             v
+-------------------------+
| Planning / Task Graph   |  <- Beads Workflow + bv
+------------+------------+
             |
             v
+-------------------------+
| Orchestration           |  <- NTM
+------------+------------+
             |
      +------+------+----------------+
      |             |                |
      v             v                v
  Claude Agent   Codex Agent    Gemini/other
      |             |                |
      +------+------+----------------+
             |
             v
+-------------------------+
| Coordination / Leases   |  <- MCP Agent Mail
+-------------------------+
| Safety Enforcement      |  <- DCG + policy gates
+-------------------------+
| Memory / Learning       |  <- CASS + CASS Memory
+-------------------------+
| Deployment              |  <- ACFS
+-------------------------+
```

Подробности: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Базовые принципы

1. **Verify before integrate.** Никакой внешний API не считается контрактом без evidence.
2. **Adapter-first.** Autopilot Core не должен зависеть от конкретного внешнего инструмента напрямую.
3. **Safety fails closed.** Отказ защитного слоя не разрешает опасные операции.
4. **Graceful degradation — только там, где это безопасно.**
5. **Auditable execution.** План, делегирование, изменения, проверки и outcomes должны быть трассируемыми.
6. **Idempotent orchestration.** Повторный запуск не должен дублировать или повреждать состояние.
7. **Human authority.** Необратимые или высокорисковые действия требуют явной политики/разрешения.
8. **Learning is evidence-based.** Память не должна превращать единичную ошибку или галлюцинацию в постоянное правило.

## Интеграции, которые планируется проверить

- [Dicklesworthstone/beads-workflow](https://github.com/Dicklesworthstone/beads-workflow)
- [Dicklesworthstone/beads_viewer](https://github.com/Dicklesworthstone/beads_viewer)
- [Dicklesworthstone/named_tmux_manager](https://github.com/Dicklesworthstone/named_tmux_manager)
- [Dicklesworthstone/mcp_agent_mail](https://github.com/Dicklesworthstone/mcp_agent_mail)
- [Dicklesworthstone/destructive_command_guard](https://github.com/Dicklesworthstone/destructive_command_guard)
- [Dicklesworthstone/coding_agent_session_search](https://github.com/Dicklesworthstone/coding_agent_session_search)
- [Dicklesworthstone/cass_memory_system](https://github.com/Dicklesworthstone/cass_memory_system)
- [Dicklesworthstone/agentic_coding_flywheel_setup](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup)

> Названия команд, MCP tools, REST routes, ports и JSON schemas не считаются подтверждёнными только потому, что упомянуты в vision или ранних заметках. Их статус ведётся в [docs/INTERFACES.md](docs/INTERFACES.md).

## Репозиторий

```text
.
├── AGENTS.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── config/
│   └── autopilot.example.yaml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── INTERFACES.md
│   ├── ROADMAP.md
│   ├── VERIFICATION.md
│   ├── VISION.md
│   └── adr/
├── scripts/
│   └── verify-integration.ps1
└── tests/
```

## Ближайший gate

Phase 0 завершается только когда:

- `autopilot-jet` имеет зафиксированный стабильный baseline;
- для каждой внешней интеграции сохранены версия/commit SHA и источники evidence;
- подтверждены реальные CLI/MCP/REST контракты;
- неизвестные интерфейсы явно помечены как UNKNOWN/PROPOSED, а не выданы за факт;
- выбран минимальный end-to-end vertical slice;
- архитектурные изменения зафиксированы ADR;
- safety policy определена до запуска мультиагентного исполнения.

До этого момента допустимы исследования, документация, протоколы проверки и безопасные scaffolds, но не production-зависимость от неподтверждённых интерфейсов.

## Лицензия

MIT — см. [LICENSE](LICENSE).
