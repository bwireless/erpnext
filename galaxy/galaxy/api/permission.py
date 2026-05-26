import frappe


def check_app_permission() -> bool:
    """Gate for the Galaxy app on the Apps screen.

    Scaffold policy: any authenticated, non-guest user can see Galaxy.
    Replace with role-based logic (e.g. "Galaxy User", "MSP Technician",
    "Client Portal User") once the role matrix is defined.
    """
    user = frappe.session.user
    return bool(user) and user != "Guest"
