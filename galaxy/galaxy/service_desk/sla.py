"""SLA engine for Galaxy Service Desk.

Responsibilities:
- On ticket create, apply the resolved SLA policy and compute response /
  resolution due timestamps from the policy's priority-keyed targets.
- On the hourly scheduler tick, recompute `sla_status` for every open
  ticket. The status transitions:
      On Track    — due time is in the future, > 25% of window remaining
      At Risk     — due time is in the future, <= 25% of window remaining
      Breached    — due time is in the past, ticket not resolved
      Met         — ticket resolved before due time
      N/A         — no SLA policy resolved (e.g. before policies exist)

The window % is computed against the resolution target, since that is
the headline number customers care about. Response-due breaches are
emitted as Frappe Realtime events but do not move `sla_status` away
from Breached/On Track for resolution.

This module is intentionally side-effect light: it never sends email or
posts to chat. Notification fan-out is wired up in the Notifications
module (later slice) by listening to the realtime events emitted here.
"""

from __future__ import annotations

import frappe
from frappe.utils import add_to_date, get_datetime, now_datetime

OPEN_STATUSES = ("Open", "In Progress", "Waiting on Customer", "Waiting on Vendor")
AT_RISK_THRESHOLD_PCT = 0.25


def resolve_policy_for_ticket(ticket) -> str | None:
    """Pick an SLA policy for a ticket.

    Order of precedence:
      1. Explicit `sla_policy` on the ticket
      2. Contract default
      3. Queue default
      4. None — ticket gets sla_status = "N/A"
    """
    if ticket.sla_policy:
        return ticket.sla_policy
    if ticket.contract:
        contract_sla = frappe.db.get_value(
            "Galaxy MSP Contract", ticket.contract, "default_sla_policy"
        )
        if contract_sla:
            return contract_sla
    if ticket.queue:
        queue_sla = frappe.db.get_value(
            "Galaxy Ticket Queue", ticket.queue, "default_sla_policy"
        )
        if queue_sla:
            return queue_sla
    return None


def _target_minutes(policy_name: str, priority: str) -> tuple[int, int] | None:
    """Return (response_minutes, resolution_minutes) for a priority."""
    rows = frappe.get_all(
        "Galaxy SLA Target",
        filters={"parent": policy_name, "priority": priority},
        fields=["response_minutes", "resolution_minutes"],
        limit=1,
    )
    if not rows:
        return None
    row = rows[0]
    return int(row.response_minutes or 0), int(row.resolution_minutes or 0)


def apply_on_create(ticket) -> None:
    """Apply SLA to a new ticket. Mutates the document in place."""
    policy = resolve_policy_for_ticket(ticket)
    if not policy:
        ticket.sla_status = "N/A"
        return

    ticket.sla_policy = policy
    targets = _target_minutes(policy, ticket.priority or "Medium")
    if not targets:
        ticket.sla_status = "N/A"
        return

    response_min, resolution_min = targets
    # `ticket.creation` is not yet set at before_insert; use wall-clock now.
    started_at = now_datetime()
    if response_min and not ticket.sla_response_due:
        ticket.sla_response_due = add_to_date(started_at, minutes=response_min)
    if resolution_min and not ticket.sla_resolution_due:
        ticket.sla_resolution_due = add_to_date(started_at, minutes=resolution_min)
    ticket.sla_status = "On Track"


def compute_status(ticket_row: dict, *, at: object | None = None) -> str:
    """Pure function: derive sla_status from a ticket row.

    `ticket_row` must contain: status, resolved_at, sla_resolution_due,
    creation. Returns one of On Track / At Risk / Breached / Met / N/A.
    """
    now = get_datetime(at) if at else now_datetime()
    due = ticket_row.get("sla_resolution_due")
    if not due:
        return "N/A"
    due = get_datetime(due)

    if ticket_row.get("status") in ("Resolved", "Closed"):
        resolved = ticket_row.get("resolved_at")
        if resolved and get_datetime(resolved) <= due:
            return "Met"
        return "Breached"

    if now >= due:
        return "Breached"

    started = get_datetime(ticket_row.get("creation"))
    total_seconds = (due - started).total_seconds()
    if total_seconds <= 0:
        # Misconfigured policy (zero/negative window). Surface as N/A
        # rather than silently parking the ticket in On Track forever.
        return "N/A"
    remaining_seconds = (due - now).total_seconds()
    if (remaining_seconds / total_seconds) <= AT_RISK_THRESHOLD_PCT:
        return "At Risk"
    return "On Track"


def tick() -> None:
    """Hourly scheduler: recompute sla_status on open tickets.

    Emits realtime events `galaxy:sla_at_risk` and `galaxy:sla_breached`
    on transitions so downstream listeners (notifications, dashboards)
    can react without polling.
    """
    rows = frappe.get_all(
        "Galaxy Ticket",
        filters={"status": ["in", OPEN_STATUSES]},
        fields=[
            "name",
            "status",
            "resolved_at",
            "sla_resolution_due",
            "sla_status",
            "creation",
            "assigned_to",
            "customer",
        ],
        limit=5000,
    )

    updated = 0
    for row in rows:
        new_status = compute_status(row)
        if new_status == row.sla_status:
            continue
        frappe.db.set_value(
            "Galaxy Ticket", row.name, "sla_status", new_status, update_modified=False
        )
        updated += 1
        if new_status in ("At Risk", "Breached"):
            frappe.publish_realtime(
                event=f"galaxy:sla_{new_status.lower().replace(' ', '_')}",
                message={
                    "ticket": row.name,
                    "customer": row.customer,
                    "assigned_to": row.assigned_to,
                    "due": str(row.sla_resolution_due),
                },
                after_commit=True,
            )

    if updated:
        frappe.db.commit()
