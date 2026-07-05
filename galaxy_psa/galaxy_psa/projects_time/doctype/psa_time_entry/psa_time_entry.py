import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours


class PSATimeEntry(Document):
	def validate(self):
		if self.start_time and self.end_time:
			self.hours = round(time_diff_in_hours(self.end_time, self.start_time), 2)

	def on_submit(self):
		self._burn_retainer()
		self._roll_up_to_ticket()

	def _burn_retainer(self):
		if not (self.billable and self.retainer_block and self.hours):
			return
		block = frappe.get_doc("Retainer Block", self.retainer_block)
		block.consumed_hours = (block.consumed_hours or 0) + self.hours
		block.save(ignore_permissions=True)

	def _roll_up_to_ticket(self):
		if not (self.ticket and self.hours):
			return
		ticket = frappe.get_doc("PSA Ticket", self.ticket)
		ticket.time_spent = (ticket.time_spent or 0) + self.hours
		ticket.save(ignore_permissions=True)
