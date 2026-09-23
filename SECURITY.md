# Security Policy

Autopilot Flywheel находится на стадии **DESIGN / FOUNDATION**. Несмотря на отсутствие production-release, вопросы безопасности считаются частью архитектуры с самого начала.

## Что относится к security issue

Особенно важны:

- возможность обхода destructive-command policy;
- privilege escalation;
- unsafe workspace access;
- silent overwrite между agents;
- утечка credentials / secrets;
- небезопасные default network bindings;
- prompt/tool injection, приводящая к опасным действиям;
- некорректная обработка approvals;
- memory poisoning / persistence of untrusted instructions;
- supply-chain risk в candidate integrations.

## Как сообщать

Если проблема содержит exploitable детали, credentials, private data или способ обхода safety guard:

1. **Не публикуйте секретные детали в обычном public issue.**
2. Используйте GitHub private vulnerability reporting / Security Advisory, если эта возможность доступна для репозитория.
3. Если private reporting недоступен, создайте минимальный public issue без exploitable payload и попросите maintainer определить приватный канал для деталей.

Для обычных архитектурных safety concerns без чувствительных деталей можно использовать public issue.

## Что приложить

По возможности укажите:

- affected commit/version;
- компонент или слой;
- preconditions;
- impact;
- минимальные шаги воспроизведения;
- ожидаемую safety policy;
- фактическое поведение;
- возможную mitigation;
- evidence без credentials.

## Security principles проекта

- destructive actions deny-by-default;
- safety-critical failure → fail closed;
- least privilege;
- explicit workspace boundaries;
- auditable approvals;
- no secret persistence in shared memory;
- no self-escalation of agent permissions;
- external interfaces verified before trust.

## Поддерживаемые версии

Production-релизов пока нет. Security fixes применяются к текущей ветке `main` и будут формализованы перед первым стабильным release.
