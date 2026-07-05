"""Recurring billing — invoked daily via scheduler_events in hooks.py."""

import frappe
from frappe.utils import getdate, today


def generate_recurring_invoices():
	"""Create Sales Invoices for Service Contracts whose next_invoice_date <= today.

	Stub: real implementation should build a Sales Invoice via
	erpnext.selling APIs, roll next_invoice_date forward by the
	billing_cycle, and email the invoice.
	"""
	due = frappe.get_all(
		"Service Contract",
		filters={"status": "Active", "next_invoice_date": ["<=", today()]},
		fields=["name", "customer", "monthly_recurring_revenue", "billing_cycle"],
		limit=500,
	)
	for c in due:
		frappe.publish_realtime("galaxy_billing_due", c)
