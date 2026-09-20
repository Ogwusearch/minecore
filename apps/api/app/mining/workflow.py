"""Mining operation workflow rules.

    draft ──record──▶ recorded ──approve──▶ approved
      │                  │
      └────cancel────────┴────cancel───▶ cancelled

Terminal states (approved, cancelled) never transition further.
Only `draft` operations are editable or deletable.
"""
from __future__ import annotations

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "draft": {"recorded", "cancelled"},
    "recorded": {"approved", "cancelled"},
    "approved": set(),
    "cancelled": set(),
}

EDITABLE_STATUSES: frozenset[str] = frozenset({"draft"})

DELETABLE_STATUSES: frozenset[str] = frozenset({"draft"})


class WorkflowError(Exception):
    """Raised when a state transition is not permitted."""


def can_transition(from_status: str, to_status: str) -> bool:
    return to_status in ALLOWED_TRANSITIONS.get(from_status, set())


def can_edit(status: str) -> bool:
    return status in EDITABLE_STATUSES


def can_delete(status: str) -> bool:
    return status in DELETABLE_STATUSES


def require_transition(from_status: str, to_status: str) -> None:
    if not can_transition(from_status, to_status):
        raise WorkflowError(
            f"Cannot transition from '{from_status}' to '{to_status}'"
        )


def require_editable(status: str) -> None:
    if not can_edit(status):
        raise WorkflowError(
            f"Operation in status '{status}' is not editable"
        )


def require_deletable(status: str) -> None:
    if not can_delete(status):
        raise WorkflowError(
            f"Operation in status '{status}' is not deletable"
        )
