app_name = "galaxy"
app_title = "Galaxy"
app_publisher = "eKosmos Inc."
app_description = "AI-first PSA & MSP/MSSP platform — galaxy.ekosmos.com"
app_email = "engineering@ekosmos.com"
app_license = "Proprietary"
app_icon = "octicon octicon-rocket"
app_color = "#5B8CFF"
app_logo_url = "/assets/galaxy/images/galaxy-logo.svg"
app_home = "/app/galaxy-dashboard"
source_link = "https://galaxy.ekosmos.com"

add_to_apps_screen = [
    {
        "name": app_name,
        "logo": app_logo_url,
        "title": app_title,
        "route": app_home,
        "has_permission": "galaxy.api.permission.check_app_permission",
    }
]

# Build pipeline
app_include_css = "galaxy.bundle.css"
app_include_js = "galaxy.bundle.js"
web_include_css = "galaxy-web.bundle.css"

# Branding overrides applied to the Desk
website_context = {
    "favicon": "/assets/galaxy/images/galaxy-favicon.svg",
    "splash_image": "/assets/galaxy/images/galaxy-logo.svg",
    "brand_html": (
        '<img src="/assets/galaxy/images/galaxy-logo.svg" '
        'alt="eKosmos Galaxy" style="height:28px;vertical-align:middle"/>'
    ),
}

# Module list — see galaxy/modules.txt
# DocTypes live under: service_desk, contracts, cmdb, knowledge_base,
# client_portal, ai_agents.

# Fixtures shipped on install (kept empty until DocTypes have JSON committed)
fixtures = []

# Permissions hook — returns True for any logged-in user during scaffold
# phase. Replace with role-based logic once the role matrix is defined.

# Scheduled tasks placeholder — wire up SLA timer, contract billing run,
# RMM sync, and AI agent scheduled runs in subsequent slices.
scheduler_events = {
    "all": [],
    "hourly": [
        # "galaxy.service_desk.sla.tick",
    ],
    "daily": [
        # "galaxy.contracts.billing.run_recurring",
        # "galaxy.cmdb.rmm.sync_assets",
    ],
}
