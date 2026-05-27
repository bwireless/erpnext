import frappe
from frappe.model.document import Document


class GalaxyTicketComment(Document):
    def after_insert(self):
        # First non-internal, non-customer comment counts as the first
        # response for SLA purposes. The "customer" side is anyone with
        # the Galaxy Portal User role; everyone else is a responder.
        if self.is_internal:
            return
        if not self.ticket:
            return
        if self.author and _is_portal_user(self.author):
            return
        ticket = frappe.get_doc("Galaxy Ticket", self.ticket)
        ticket.mark_first_response(self.author or frappe.session.user)


def _is_portal_user(user: str) -> bool:
    return bool(
        frappe.db.exists(
            "Has Role",
            {"parent": user, "parenttype": "User", "role": "Galaxy Portal User"},
        )
    )
