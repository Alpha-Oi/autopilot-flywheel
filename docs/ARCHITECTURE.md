# Архитектура Autopilot Flywheel

Требует верификации после завершения autopilot-jet.

## Слои

1. Ядро — Autopilot Core
2. Планирование — Beads Workflow, Beads Viewer
3. Оркестрация — NTM
4. Координация — MCP Agent Mail
5. Защита — DCG
6. Память — CASS, CASS Memory
7. Развёртывание — ACFS

## Принципы

- Каждый слой независим
- Graceful degradation
- Идемпотентность
- Аудит через Agent Mail

## Требует верификации

- [ ] API Autopilot Core
- [ ] Формат обмена с Beads
- [ ] MCP-ресурсы Agent Mail
- [ ] Схема данных CASS Memory
- [ ] Robot-mode API NTM
- [ ] Точки встраивания DCG
