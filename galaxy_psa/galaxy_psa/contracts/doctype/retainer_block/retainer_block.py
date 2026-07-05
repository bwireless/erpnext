from frappe.model.document import Document


class RetainerBlock(Document):
	def before_save(self):
		self.remaining_hours = max(0.0, (self.purchased_hours or 0) - (self.consumed_hours or 0))
		if self.remaining_hours == 0 and self.status == "Active":
			self.status = "Exhausted"
