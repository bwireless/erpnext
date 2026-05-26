import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class GalaxyTicket(Document):
    """Service desk ticket.

    Heavy logic (SLA timers, escalation, AI summarization) is deferred.
    The hooks below mark the seams those features will plug into so the
    scaffold remains forward-compatible with the planned modules.
    """

    def validate(self):
        self._stamp_response_and_resolution()

    def _stamp_response_and_resolution(self):
        if self.has_value_changed("status"):
            if self.status in ("Resolved", "Closed") and not self.resolved_at:
                self.resolved_at = now_datetime()
                if self.sla_resolution_due:
                    self.sla_status = (
                        "Met" if now_datetime() <= self.sla_resolution_due
                        else "Breached"
                    )

    def has_value_changed(self, fieldname: str) -> bool:
        if self.is_new():
            return bool(self.get(fieldname))
        old = self.get_doc_before_save()
        return bool(old) and old.get(fieldname) != self.get(fieldname)
