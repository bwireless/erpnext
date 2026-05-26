from frappe import _, throw
from frappe.model.document import Document


class GalaxyAIAgent(Document):
    """AI agent definition.

    The agent is configuration only; execution is performed by the
    runner in `galaxy.ai_agents.runner` (not yet implemented). Each
    invocation produces a Galaxy AI Agent Run record.
    """

    def validate(self):
        if self.temperature is not None and not (0 <= self.temperature <= 2):
            throw(_("Temperature must be between 0 and 2."))
        if self.thinking_enabled and (self.thinking_budget_tokens or 0) <= 0:
            throw(_("Thinking budget must be > 0 when Extended Thinking is on."))
