"""Ticket assignment policies.

Least-loaded per queue: when a ticket is created with a queue but no
explicit assignee, pick the enabled Galaxy Technician with the fewest
currently-open tickets in that queue. The queue's `default_assignee`
overrides the load-balancing pick.

(Pure round-robin / FIFO rotation is intentionally not used — uneven
ticket sizes would leave busy technicians starved. Swap to FIFO only
if you also add an explicit `last_assigned_at` tracker per queue.)
"""

from __future__ import annotations

import frappe


def pick_assignee_for_queue(queue_name: str) -> str | None:
    """Round-robin pick. Returns the next user, or None if no roster."""
    queue = frappe.db.get_value(
        "Galaxy Ticket Queue", queue_name, ["default_assignee"], as_dict=True
    )
    if queue and queue.default_assignee:
        return queue.default_assignee

    technicians = _technician_roster()
    if not technicians:
        return None

    # Pick the technician with the fewest open tickets in this queue.
    counts = frappe.db.sql(
        """
        SELECT t.assigned_to, COUNT(*) AS open_count
        FROM `tabGalaxy Ticket` t
        WHERE t.queue = %s
          AND t.status NOT IN ('Resolved', 'Closed', 'Cancelled')
          AND t.assigned_to IN %s
        GROUP BY t.assigned_to
        """,
        (queue_name, tuple(technicians)),
        as_dict=True,
    )
    load = {row.assigned_to: row.open_count for row in counts}
    return min(technicians, key=lambda u: load.get(u, 0))


def _technician_roster() -> list[str]:
    rows = frappe.get_all(
        "Has Role",
        filters={"role": "Galaxy Technician", "parenttype": "User"},
        fields=["parent as user"],
    )
    if not rows:
        return []
    users = [r.user for r in rows]
    enabled = frappe.get_all(
        "User",
        filters={"name": ["in", users], "enabled": 1},
        pluck="name",
    )
    return enabled


def assign_on_create(ticket) -> None:
    """Auto-assign a new ticket if it has a queue but no assignee."""
    if ticket.assigned_to or not ticket.queue:
        return
    pick = pick_assignee_for_queue(ticket.queue)
    if pick:
        ticket.assigned_to = pick
