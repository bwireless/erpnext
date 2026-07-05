from frappe.model.document import Document


class ServiceContract(Document):
	def validate(self):
		if self.end_date and self.start_date and self.end_date < self.start_date:
			from frappe import throw
			throw("Contract end date cannot be before the start date.")
