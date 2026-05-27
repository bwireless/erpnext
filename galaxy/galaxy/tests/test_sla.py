"""Unit tests for galaxy.service_desk.sla.compute_status.

Pure function tests — no Frappe DB needed. Run with:
    bench --site <site> run-tests --app galaxy --module galaxy.tests.test_sla
"""

from __future__ import annotations

import unittest
from datetime import datetime, timedelta

from galaxy.service_desk.sla import compute_status


def _row(created_ago_min: int, due_in_min: int, status: str = "Open", resolved_at=None) -> dict:
    now = datetime(2026, 5, 26, 12, 0, 0)
    return {
        "creation": now - timedelta(minutes=created_ago_min),
        "sla_resolution_due": now + timedelta(minutes=due_in_min),
        "status": status,
        "resolved_at": resolved_at,
    }


_NOW = datetime(2026, 5, 26, 12, 0, 0)


class ComputeStatusTests(unittest.TestCase):
    def test_no_due_returns_na(self):
        row = {"status": "Open", "resolved_at": None, "sla_resolution_due": None, "creation": _NOW}
        self.assertEqual(compute_status(row, at=_NOW), "N/A")

    def test_on_track_when_plenty_of_window_left(self):
        # created 1 min ago, due in 100 min → 99% remaining
        row = _row(created_ago_min=1, due_in_min=100)
        self.assertEqual(compute_status(row, at=_NOW), "On Track")

    def test_at_risk_when_under_25pct_remaining(self):
        # created 90 min ago, due in 10 min → 10% of a 100-min window
        row = _row(created_ago_min=90, due_in_min=10)
        self.assertEqual(compute_status(row, at=_NOW), "At Risk")

    def test_breached_when_past_due_unresolved(self):
        row = _row(created_ago_min=120, due_in_min=-10)
        self.assertEqual(compute_status(row, at=_NOW), "Breached")

    def test_met_when_resolved_before_due(self):
        row = _row(
            created_ago_min=60,
            due_in_min=30,
            status="Resolved",
            resolved_at=_NOW - timedelta(minutes=5),
        )
        self.assertEqual(compute_status(row, at=_NOW), "Met")

    def test_breached_at_exact_due_time(self):
        # now == due, ticket still open → Breached, not At Risk
        row = _row(created_ago_min=60, due_in_min=0)
        self.assertEqual(compute_status(row, at=_NOW), "Breached")

    def test_zero_window_returns_na(self):
        # Misconfigured policy: due == creation
        row = {
            "status": "Open",
            "resolved_at": None,
            "sla_resolution_due": _NOW + timedelta(minutes=10),
            "creation": _NOW + timedelta(minutes=10),
        }
        self.assertEqual(compute_status(row, at=_NOW), "N/A")

    def test_resolved_after_due_is_breached(self):
        row = _row(
            created_ago_min=120,
            due_in_min=-20,
            status="Resolved",
            resolved_at=_NOW - timedelta(minutes=5),
        )
        self.assertEqual(compute_status(row, at=_NOW), "Breached")


if __name__ == "__main__":
    unittest.main()
