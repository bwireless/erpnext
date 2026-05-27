import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

from galaxy.service_desk import assignment, sla


class GalaxyTicket(Document):
    """Service desk ticket.

    Lifecycle:
    - before_insert: apply SLA, auto-assign from queue
    - validate: stamp resolved_at and finalize sla_status on close
    - on_update: stamp first_response_at when a non-customer comment lands
      (the comment doc calls back into here)
    """

    def before_insert(self):
        sla.apply_on_create(self)
        assignment.assign_on_create(self)

    def validate(self):
        self._stamp_resolution()

    def _stamp_resolution(self):
        if not self.has_value_changed("status"):
            return
        if self.status in ("Resolved", "Closed") and not self.resolved_at:
            self.resolved_at = now_datetime()
            if self.sla_resolution_due:
                self.sla_status = sla.compute_status(
                    {
                        "status": self.status,
                        "resolved_at": self.resolved_at,
                        "sla_resolution_due": self.sla_resolution_due,
                        "creation": self.creation or now_datetime(),
                    }
                )

    def has_value_changed(self, fieldname: str) -> bool:
        if self.is_new():
            return bool(self.get(fieldname))
        old = self.get_doc_before_save()
        return bool(old) and old.get(fieldname) != self.get(fieldname)

    def mark_first_response(self, responder: str) -> None:
        """Called when a non-customer comment is added."""
        if self.first_response_at:
            return
        self.db_set("first_response_at", now_datetime(), update_modified=False)
        if self.sla_response_due and self.first_response_at > self.sla_response_due:
            frappe.publish_realtime(
                event="galaxy:sla_response_breached",
                message={"ticket": self.name, "responder": responder},
                after_commit=True,
            )
