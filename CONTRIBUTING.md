# Contributing to Autopilot Flywheel

Спасибо за интерес к проекту. Сейчас Autopilot Flywheel находится на стадии **vision / architecture / verification foundation**.

## Перед началом

Прочитайте:

1. [docs/VISION.md](docs/VISION.md)
2. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
3. [docs/INTERFACES.md](docs/INTERFACES.md)
4. [docs/VERIFICATION.md](docs/VERIFICATION.md)
5. [AGENTS.md](AGENTS.md)

## Что особенно полезно сейчас

- проверка реальных интерфейсов upstream-проектов;
- фиксация версий, commit SHA и compatibility notes;
- architecture review;
- threat modeling и safety design;
- contract tests и безопасные verification scripts;
- документация;
- ADR для важных решений.

До Phase 0 Gate не следует добавлять крупную production-реализацию, зависящую от неподтверждённых внешних интерфейсов.

## Issues

Для предложения используйте понятный scope:

- `architecture` — изменение границ или системного дизайна;
- `integration` — внешний инструмент/API/MCP;
- `verification` — подтверждение или опровержение assumptions;
- `safety` — политики, guards, destructive actions;
- `docs` — документация;
- `benchmark` — измеримые сравнения.

Фактические баги и подтверждённые несовместимости отделяйте от гипотез.

## Branch naming

Рекомендуемые префиксы:

- `docs/<topic>`
- `arch/<topic>`
- `verify/<integration>`
- `feat/<topic>`
- `fix/<topic>`
- `test/<topic>`

## Commit messages

Используйте короткие атомарные сообщения, например:

```text
docs: define integration verification protocol
arch: formalize adapter boundary
verify: confirm NTM capability surface
test: add destructive-command guard cases
```

## Pull Request checklist

PR должен объяснять:

- цель;
- изменённые файлы;
- что является FACT, PROPOSED и UNKNOWN;
- какие проверки выполнены;
- какие внешние версии/commit SHA использованы;
- есть ли новые safety implications;
- требуется ли ADR;
- что осталось сделать.

Для внешней интеграции PR без evidence не должен менять статус на VERIFIED.

## Architecture Decision Records

ADR обязателен для значимых решений. См. [docs/adr/README.md](docs/adr/README.md).

Номер ADR назначается последовательно:

```text
docs/adr/0001-short-title.md
docs/adr/0002-short-title.md
```

## Совместимость

Не проектируйте Core вокруг случайной версии стороннего инструмента.

Предпочтительно:

- capability discovery;
- adapters;
- version pinning;
- explicit compatibility checks;
- feature flags;
- safe fallback.

## Безопасность

Не публикуйте и не коммитьте:

- API keys;
- access tokens;
- private keys;
- credentials;
- реальные секреты из `.env`;
- конфиденциальные session dumps.

Не отключайте safety guard ради прохождения тестов.

## Лицензия

Внося вклад, вы соглашаетесь, что он распространяется на условиях MIT License проекта.
