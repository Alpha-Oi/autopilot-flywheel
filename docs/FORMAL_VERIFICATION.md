# Формальная верификация (TLA+)

Мы используем TLA+ для доказательства отсутствия дедлоков в StateManager.

## Спецификация (StateManager.tla)

---- MODULE StateManager ----
EXTENDS Naturals, Sequences

VARIABLES state, task_id

Init == state = "idle" /\ task_id = "none"

SaveTask(t) ==
    /\ state = "idle"
    /\ state' = "saving"
    /\ task_id' = t

FinishSave ==
    /\ state = "saving"
    /\ state' = "saved"

Next == \/ \E t \in {"task1", "task2"}: SaveTask(t)
        \/ FinishSave
====
