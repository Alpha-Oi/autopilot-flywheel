# Интерфейсы

ТРЕБУЕТ ВЕРИФИКАЦИИ после завершения autopilot-jet.

## Core <-> Beads Workflow
autopilot core --emit-spec spec.md
beads-workflow convert spec.md --output tasks.beads

## Core <-> Beads Viewer
bv --robot-triage --json

## Core <-> NTM
ntm spawn <session> --cc=<n> --cod=<n> --agy=<n>
ntm send <session> "<task>"
ntm work next
ntm work triage

## Core <-> Agent Mail
MCP (HTTP). Ресурсы: inbox, outbox, file leases.

## Core <-> CASS Memory
cm context "<task>" --json
cm outcome --task-id <id> --status success|failure
cm feedback --rule-id <id> --signal positive|negative

Ответ cm context:
{
  "rules": [{"id": "...", "text": "...", "confidence": 0.92}],
  "similar_tasks": [],
  "episodic_hits": []
}

## Core <-> DCG
dcg scan <command>

## Core <-> ACFS
curl -fsSL ".../install.sh" | bash

## Чек-лист верификации
- [ ] Флаги bv --robot-*
- [ ] MCP-инструменты Agent Mail
- [ ] Формат cm context
- [ ] REST API NTM
- [ ] Точки встраивания DCG
