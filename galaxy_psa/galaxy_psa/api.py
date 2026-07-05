"""Public whitelisted API surface for Galaxy PSA.

Everything here is either called from JS (@frappe.whitelist decorated)
or wired up from hooks.py.
"""

from __future__ import annotations

import frappe


def check_app_permission():
	"""Gate the Galaxy app tile on the Apps screen."""
	roles = set(frappe.get_roles(frappe.session.user))
	allowed = {
		"Galaxy Technician",
		"Galaxy Dispatcher",
		"Galaxy Service Manager",
		"Galaxy Security Analyst",
		"System Manager",
		"Administrator",
	}
	return bool(roles & allowed)


@frappe.whitelist()
def brand():
	"""Return the current brand tokens. Client fetches this on login."""
	return {
		"product_name": "Galaxy",
		"vendor": "eKosmos Inc.",
		"colors": {
			"deep_space": "#0B1026",
			"nebula": "#1B2451",
			"electron": "#7B5CFF",
			"supernova": "#37E2D5",
			"solar": "#FFC857",
			"nova": "#FF5D8F",
		},
		"logo": "/assets/galaxy_psa/images/galaxy-logo.svg",
	}
