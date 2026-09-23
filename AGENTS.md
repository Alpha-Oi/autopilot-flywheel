# AGENTS.md — Autopilot Flywheel

Этот файл задаёт обязательные правила для Codex, Claude Code, Gemini CLI и любых других coding agents, работающих в этом репозитории.

## 1. Текущий режим проекта

**PROJECT_STATE = DESIGN_FOUNDATION**

До прохождения Phase 0 Verification Gate агент НЕ должен превращать архитектурные предположения в рабочие зависимости.

Разрешено:

- улучшать документацию и архитектуру;
- исследовать upstream-проекты;
- собирать evidence;
- писать безопасные verification tooling/scaffolds;
- проектировать внутренние adapter contracts;
- добавлять тестовые фикстуры, не утверждающие неподтверждённые внешние API.

Не разрешено без отдельного задания и evidence:

- реализовывать production integration против предполагаемого CLI/API;
- закреплять выдуманные ports/routes/tool names;
- автоматически устанавливать или запускать сторонний код;
- менять upstream-зависимости "на глаз";
- выполнять destructive Git/filesystem operations.

## 2. Иерархия источников истины

При конфликте руководствуйся в таком порядке:

1. Явная текущая задача пользователя/maintainer.
2. `AGENTS.md`.
3. `docs/ARCHITECTURE.md`.
4. `docs/INTERFACES.md` — для внешних контрактов.
5. `docs/ROADMAP.md`.
6. `docs/VISION.md` — продуктовый intent.
7. README и остальные заметки.

Vision определяет **куда идём**, но не гарантирует, что перечисленный там внешний API существует в указанной форме.

## 3. Обязательный workflow агента

Перед изменением:

1. Прочитать `README.md`, `AGENTS.md` и относящиеся к задаче docs.
2. Проверить текущее состояние репозитория.
3. Классифицировать работу: docs / verification / architecture / implementation / safety-critical.
4. Для внешней интеграции открыть `docs/INTERFACES.md` и определить её статус.
5. Если статус не VERIFIED, сначала собрать evidence; не кодировать гипотезу как факт.
6. Выбрать минимальный change set.
7. Выполнить проверки, соответствующие изменению.
8. В конце перечислить: что изменено, что проверено, что осталось неизвестным.

## 4. Правило внешних интерфейсов

Каждый внешний контракт должен иметь:

- upstream repository;
- pinned version/tag/commit SHA;
- дату проверки;
- источник evidence;
- фактический способ вызова;
- фактические input/output/error semantics;
- статус: PROPOSED / VERIFIED / IMPLEMENTED / DEPRECATED;
- compatibility notes.

Если хотя бы один пункт неизвестен — контракт не считается VERIFIED.

Запрещено выдавать пример из README, старого issue, памяти модели или vision за фактический API без проверки.

## 5. Adapter-first архитектура

Autopilot Core должен обращаться к внешним системам через внутренние capability adapters.

Ожидаемая форма границы:

```text
Core -> internal capability contract -> adapter -> external tool
```

Нельзя распространять vendor-specific структуры по всему core.

Если внешний инструмент заменяется, изменения должны локализоваться в adapter/integration boundary.

## 6. Safety invariants

Всегда:

- destructive operations запрещены по умолчанию;
- safety-critical dependency failure = fail closed;
- никакого `rm -rf`, `git reset --hard`, force push или очистки workspace без явного разрешения;
- секреты не коммитятся;
- агент не должен обходить hooks/guards ради "успешного" теста;
- file lease / ownership conflicts должны считаться блокирующим сигналом;
- high-risk actions должны быть auditable.

Graceful degradation не применяется к действию, если деградация снимает обязательную защиту.

## 7. Мультиагентные правила

До запуска нескольких агентов должны существовать:

- task identity;
- ownership/lease strategy;
- dependency awareness;
- shared-state rules;
- conflict policy;
- completion/outcome protocol;
- audit trail.

Два агента не должны одновременно редактировать один и тот же mutable scope без координации.

## 8. Memory / learning rules

Нельзя автоматически превращать любую успешную или неуспешную сессию в постоянное правило.

Процедурная память должна хранить provenance и confidence. Новое правило должно иметь возможность быть:

- подтверждено;
- понижено в confidence;
- опровергнуто;
- заменено;
- удалено.

Outcome без проверки результата — слабое evidence.

## 9. Изменения архитектуры

Изменение одного из пунктов ниже требует ADR:

- границы слоёв;
- источник истины;
- основной runtime/orchestrator;
- модель состояния;
- safety policy;
- формат persistent data;
- обязательная внешняя зависимость;
- compatibility/versioning policy.

Используй `docs/adr/0000-template.md`.

## 10. Проверки

Docs-only изменение:

- проверить ссылки и внутреннюю непротиворечивость;
- убедиться, что PROPOSED не выдано за VERIFIED.

Integration изменение:

- пройти `docs/VERIFICATION.md`;
- сохранить evidence;
- добавить/обновить контракт в `docs/INTERFACES.md`;
- добавить contract/integration tests до включения по умолчанию.

Safety изменение:

- positive tests;
- negative tests;
- bypass tests;
- failure-mode tests.

## 11. Commit discipline

Предпочтительны небольшие атомарные commits:

- `docs:`
- `arch:`
- `verify:`
- `feat:`
- `fix:`
- `test:`
- `chore:`

Не смешивать архитектурное решение, массовый рефакторинг и новую интеграцию без необходимости.

## 12. Definition of Done

Задача не завершена, пока агент не может ответить:

- Что изменилось?
- Почему?
- Какими источниками/тестами это подтверждено?
- Какие assumptions остались?
- Какие safety implications появились?
- Нужно ли обновить INTERFACES, ROADMAP или ADR?
