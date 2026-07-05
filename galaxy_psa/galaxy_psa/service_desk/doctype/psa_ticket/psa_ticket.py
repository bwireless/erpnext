import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class PSATicket(Document):
	def validate(self):
		self._apply_sla()
		self._stamp_status_transitions()

	def _apply_sla(self):
		if self.sla_policy and not self.response_by:
			policy = frappe.get_cached_doc("SLA Policy", self.sla_policy)
			self.response_by, self.resolution_by = policy.compute_targets(self.creation or now_datetime())

	def _stamp_status_transitions(self):
		if self.has_value_changed("status"):
			if self.status == "Resolved" and not self.resolved_on:
				self.resolved_on = now_datetime()
			if self.status == "Closed" and not self.closed_on:
				self.closed_on = now_datetime()
