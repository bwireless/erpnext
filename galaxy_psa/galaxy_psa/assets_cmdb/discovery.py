"""RMM inventory reconciliation — invoked daily via scheduler_events."""

import frappe


def reconcile_rmm_inventory():
	"""Pull inventory from configured RMMs and upsert Configuration Items.

	Stub: real implementation should hit NinjaOne/Datto RMM/Auvik APIs
	via keys stored in a `RMM Integration Settings` Single (not yet
	created), then upsert Configuration Item rows keyed on
	(rmm_source, rmm_id).
	"""
	frappe.logger("galaxy").info("Galaxy RMM discovery: not yet implemented")
