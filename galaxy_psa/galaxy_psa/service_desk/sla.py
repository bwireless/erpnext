"""SLA housekeeping — invoked hourly via scheduler_events in hooks.py."""

import frappe
from frappe.utils import now_datetime


def check_sla_breaches():
	"""Flag tickets past their response/resolution targets.

	Stub: real implementation should raise Notification Log entries and
	trigger the escalation rules on SLA Policy.
	"""
	now = now_datetime()
	overdue = frappe.get_all(
		"PSA Ticket",
		filters={"status": ["not in", ["Resolved", "Closed", "Cancelled"]]},
		or_filters=[["response_by", "<", now], ["resolution_by", "<", now]],
		fields=["name", "assigned_to", "sla_policy", "response_by", "resolution_by"],
		limit=500,
	)
	for t in overdue:
		frappe.publish_realtime("galaxy_sla_breach", t, user=t.assigned_to)
