from frappe.model.document import Document


class GalaxyMSPContract(Document):
    def validate(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            from frappe import throw, _
            throw(_("Contract end date cannot be before start date."))
