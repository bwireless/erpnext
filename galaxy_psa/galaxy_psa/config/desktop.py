from frappe import _


def get_data():
	return [
		{"module_name": "Service Desk", "category": "Modules", "label": _("Service Desk"),
		 "color": "#7B5CFF", "icon": "octicon octicon-issue-opened", "type": "module",
		 "description": "Tickets, SLAs, queues, escalations."},
		{"module_name": "Contracts", "category": "Modules", "label": _("Contracts"),
		 "color": "#37E2D5", "icon": "octicon octicon-file-text", "type": "module",
		 "description": "Service contracts, retainers, block-hours, recurring billing."},
		{"module_name": "Assets CMDB", "category": "Modules", "label": _("Assets / CMDB"),
		 "color": "#FFC857", "icon": "octicon octicon-server", "type": "module",
		 "description": "Configuration items, RMM integrations, discovery."},
		{"module_name": "Projects Time", "category": "Modules", "label": _("Projects & Time"),
		 "color": "#FF5D8F", "icon": "octicon octicon-checklist", "type": "module",
		 "description": "Project templates, time entries, utilization."},
		{"module_name": "CPQ", "category": "Modules", "label": _("Quoting / CPQ"),
		 "color": "#7B5CFF", "icon": "octicon octicon-tag", "type": "module",
		 "description": "Configure-price-quote, distributor catalogs, approvals."},
		{"module_name": "Client Portal", "category": "Modules", "label": _("Client Portal"),
		 "color": "#37E2D5", "icon": "octicon octicon-organization", "type": "module",
		 "description": "Branded customer self-service."},
		{"module_name": "AI", "category": "Modules", "label": _("AI"),
		 "color": "#7B5CFF", "icon": "octicon octicon-hubot", "type": "module",
		 "description": "Claude-powered triage, summarization, runbooks."},
		{"module_name": "Compliance", "category": "Modules", "label": _("Compliance (MSSP)"),
		 "color": "#FF5D8F", "icon": "octicon octicon-shield", "type": "module",
		 "description": "SOC2 / CIS / NIST / ISO27001 frameworks and controls."},
	]
