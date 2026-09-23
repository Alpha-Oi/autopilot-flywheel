# Autopilot Flywheel

> Мультиагентная самообучающаяся платформа для автономной разработки ПО.
> Эволюция [autopilot-jet](https://github.com/Alpha-Oi/autopilot-jet) на базе экосистемы [Dicklesworthstone](https://github.com/Dicklesworthstone).

## ВАЖНО: ВЕРИФИКАЦИЯ ПОСЛЕ ЗАВЕРШЕНИЯ autopilot-jet

Этот репозиторий — vision document и карта интеграции.

Реальная разработка начнётся **только после того, как основной проект [autopilot-jet](https://github.com/Alpha-Oi/autopilot-jet) будет полностью завершён и стабилен.**

После готовности `autopilot-jet` необходимо повторно проверить ВСЮ архитектуру, интерфейсы, предположения и схемы данных.

- Проверить актуальность API каждого из 7 инструментов
- Проверить совместимость версий и зависимостей
- Проверить реальные форматы обмена данными (JSON-схемы, MCP-ресурсы)
- Проверить, что архитектура Autopilot Core не изменилась
- Проверить пути интеграции на реальных примерах
- Обновить этот README и `docs/INTERFACES.md`

**Статус:** Ожидание завершения `autopilot-jet` -> фаза верификации -> разработка.

## Что это

Autopilot Flywheel превращает одиночного AI-агента в рой координируемых агентов, работающих параллельно над одной кодовой базой, с общей памятью, защитой от конфликтов и способностью учиться на собственном опыте.

Платформа объединяет 7 инструментов:

1. **Beads Workflow** — декомпозиция плана в задачи
2. **Beads Viewer (bv)** — граф зависимостей и приоритизация
3. **NTM** — оркестрация агентов в tmux
4. **MCP Agent Mail** — координация и файловые аренды
5. **DCG** — защита от деструктивных команд
6. **CASS + CASS Memory** — память и самообучение
7. **ACFS** — воспроизводимое развёртывание

## Слои

- **Ядро:** Autopilot Core
- **1. Планирование:** Beads Workflow, Beads Viewer
- **2. Оркестрация:** NTM
- **3. Координация:** MCP Agent Mail
- **3. Защита:** DCG
- **4. Память:** CASS, CASS Memory
- **5. Развёртывание:** ACFS

## Поток данных

1. Запрос
2. Планирование (Autopilot Core + Beads)
3. Контекст (CASS Memory -> cm context)
4. Запуск (NTM + Agent Mail)
5. Выполнение (агенты + DCG)
6. Проверка (Autopilot Core)
7. Обучение (CASS + CASS Memory -> cm outcome)

## Дорожная карта

### Фаза 0 — Ожидание и верификация
- [x] Vision document
- [ ] Завершение autopilot-jet
- [ ] Верификация архитектуры
- [ ] Проверка API всех 7 инструментов
- [ ] Обновление docs/INTERFACES.md

### Этап 1 — Безопасность (DCG)
### Этап 2 — Память (CASS + CASS Memory)
### Этап 3 — Планирование (Beads)
### Этап 4 — Оркестрация (NTM)
### Этап 5 — Координация (Agent Mail)
### Этап 6 — Развёртывание (ACFS)
### Этап 7 — Продукт (v1.0)

## Зависимости

- [Dicklesworthstone/beads-workflow](https://github.com/Dicklesworthstone/beads-workflow)
- [Dicklesworthstone/beads_viewer](https://github.com/Dicklesworthstone/beads_viewer)
- [Dicklesworthstone/named_tmux_manager](https://github.com/Dicklesworthstone/named_tmux_manager)
- [Dicklesworthstone/mcp_agent_mail](https://github.com/Dicklesworthstone/mcp_agent_mail)
- [Dicklesworthstone/destructive_command_guard](https://github.com/Dicklesworthstone/destructive_command_guard)
- [Dicklesworthstone/coding_agent_session_search](https://github.com/Dicklesworthstone/coding_agent_session_search)
- [Dicklesworthstone/cass_memory_system](https://github.com/Dicklesworthstone/cass_memory_system)
- [Dicklesworthstone/agentic_coding_flywheel_setup](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup)

## Лицензия

MIT
