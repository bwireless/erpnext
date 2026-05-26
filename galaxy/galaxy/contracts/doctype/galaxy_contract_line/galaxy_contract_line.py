from frappe.model.document import Document


class GalaxyContractLine(Document):
    def validate(self):
        self.amount = (self.quantity or 0) * (self.rate or 0)
