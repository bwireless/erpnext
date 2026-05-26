import json

from frappe import _, throw
from frappe.model.document import Document


class GalaxyAIAgentTool(Document):
    def validate(self):
        if self.config_json:
            try:
                json.loads(self.config_json)
            except json.JSONDecodeError as exc:
                throw(_("Tool config is not valid JSON: {0}").format(exc))
