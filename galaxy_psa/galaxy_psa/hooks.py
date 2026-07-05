app_name = "galaxy_psa"
app_title = "Galaxy"
app_publisher = "eKosmos Inc."
app_description = "Galaxy PSA — AI-first Professional Services Automation for MSP/MSSPs"
app_email = "engineering@ekosmos.com"
app_license = "Proprietary"
app_icon_url = "/assets/galaxy_psa/images/galaxy-logo.svg"
app_logo_url = "/assets/galaxy_psa/images/galaxy-logo.svg"
app_home = "/app/galaxy-workspace"
source_link = "https://galaxy.ekosmos.com"

# The favicon and login page pull from the same tokens defined in
# galaxy_brand.css so brand swaps stay in one place.
app_include_css = "/assets/galaxy_psa/css/galaxy_brand.css"
app_include_js = "/assets/galaxy_psa/js/galaxy_desk.js"
web_include_css = "/assets/galaxy_psa/css/galaxy_brand.css"

website_context = {
	"favicon": "/assets/galaxy_psa/images/galaxy-favicon.svg",
	"splash_image": "/assets/galaxy_psa/images/galaxy-logo.svg",
	"brand_html": '<img src="/assets/galaxy_psa/images/galaxy-logo.svg" alt="Galaxy by eKosmos" style="height:28px">',
}

add_to_apps_screen = [
	{
		"name": app_name,
		"logo": app_logo_url,
		"title": app_title,
		"route": app_home,
		"has_permission": "galaxy_psa.api.check_app_permission",
	}
]

boot_session = "galaxy_psa.boot.boot_session"

# Fixtures shipped with the app on install.
fixtures = [
	{"dt": "Role", "filters": [["name", "in", [
		"Galaxy Technician",
		"Galaxy Dispatcher",
		"Galaxy Service Manager",
		"Galaxy Client Contact",
		"Galaxy Security Analyst",
	]]]},
]

# --- Scheduled Events ------------------------------------------------
scheduler_events = {
	"hourly": [
		"galaxy_psa.service_desk.sla.check_sla_breaches",
	],
	"daily": [
		"galaxy_psa.contracts.billing.generate_recurring_invoices",
		"galaxy_psa.assets_cmdb.discovery.reconcile_rmm_inventory",
	],
	"cron": {
		# every 5 minutes: pull email tickets, run AI triage
		"*/5 * * * *": [
			"galaxy_psa.ai.triage.run_pending_triage",
		],
	},
}

# --- Portal ----------------------------------------------------------
standard_portal_menu_items = [
	{"title": "My Tickets", "route": "/tickets", "role": "Galaxy Client Contact"},
	{"title": "My Assets", "route": "/my-assets", "role": "Galaxy Client Contact"},
	{"title": "Contracts", "route": "/my-contracts", "role": "Galaxy Client Contact"},
	{"title": "Invoices", "route": "/invoices", "role": "Galaxy Client Contact"},
	{"title": "Knowledge Base", "route": "/kb"},
]

# --- Overrides -------------------------------------------------------
override_whitelisted_methods = {}
