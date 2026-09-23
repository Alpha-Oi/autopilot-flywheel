# Architecture Decision Records

ADR фиксируют значимые архитектурные решения Autopilot Flywheel.

## Когда нужен ADR

ADR обязателен, если меняется:

- системная граница;
- обязательный upstream;
- runtime;
- persistence;
- event model;
- security policy;
- public/stable interface;
- orchestration model;
- memory model;
- deployment topology.

## Именование

```text
0001-short-title.md
0002-short-title.md
```

Не переиспользуйте номер удалённого ADR.

## Статусы

- Proposed
- Accepted
- Superseded
- Rejected
- Deprecated

## Процесс

1. Скопировать `0000-template.md`.
2. Описать context и decision drivers.
3. Перечислить alternatives.
4. Отдельно указать safety/compatibility consequences.
5. Получить review.
6. После принятия обновить связанные architecture/interfaces docs.
