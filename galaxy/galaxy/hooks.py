app_name = "galaxy"
app_title = "Galaxy"
app_publisher = "eKosmos Inc."
app_description = "AI-first PSA & MSP/MSSP platform — galaxy.ekosmos.com"
app_email = "engineering@ekosmos.com"
app_license = "Proprietary"
app_icon = "octicon octicon-rocket"
app_color = "#5B8CFF"
app_logo_url = "/assets/galaxy/images/galaxy-logo.svg"
app_home = "/app/galaxy"
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

fixtures = []

# Scheduler events. SLA recompute runs hourly; the daily slots are
# placeholders the next slices fill in.
scheduler_events = {
    "hourly": [
        "galaxy.service_desk.sla.tick",
    ],
    "daily": [
        # "galaxy.contracts.billing.run_recurring",
        # "galaxy.cmdb.rmm.sync_all",
    ],
}
