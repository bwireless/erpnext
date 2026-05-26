import re

from frappe.model.document import Document
from frappe.utils import now_datetime


class GalaxyKBArticle(Document):
    def validate(self):
        if not self.slug and self.title:
            self.slug = re.sub(r"[^a-z0-9]+", "-", self.title.lower()).strip("-")
        if self.status == "Published" and not self.published_at:
            self.published_at = now_datetime()
