from frappe.model.document import Document


class PSAQuote(Document):
	def before_save(self):
		self.total = (self.subtotal or 0) + (self.tax_total or 0)
