"""Galaxy AI Agent runner — execution engine for Galaxy AI Agent.

This module is the seam between agent definitions and live model calls.
It is intentionally a stub at scaffold time; the next slice will wire it
to the Anthropic SDK (and optional Azure OpenAI / OpenAI providers) and
record results into Galaxy AI Agent Run / Galaxy AI Agent Message.

Design intent (recorded so the next slice has direction, not a wishlist):

- `run(agent_name, input_payload, *, user=None)` enqueues a run, returns
  the Run name. Synchronous mode is allowed for short interactive calls.
- Tool dispatch lives in `tools.py` (one resolver per tool_type from the
  Galaxy AI Agent Tool DocType). The default Frappe tools enforce the
  caller's permission set; HTTP tools honor `allow_external_calls`.
- Model selection respects the agent's `provider` + `model` fields.
  Default to claude-opus-4-7 for high-complexity agents,
  claude-sonnet-4-6 for default, claude-haiku-4-5 for high-volume cheap
  agents.
- Prompt caching is mandatory for any agent whose system_prompt is
  > 1024 tokens — cache the system block and any tool schemas.
- Cost accounting writes back to Galaxy AI Agent Run.cost_usd and
  increments Galaxy AI Agent.total_*_tokens.
"""

import frappe


def run(agent_name: str, input_payload: dict, *, user: str | None = None) -> str:
    """Execute an agent. Returns the Galaxy AI Agent Run name.

    Not implemented in the scaffold. Raises NotImplementedError so any
    caller that wires up to it before the runner lands fails loudly.
    """
    frappe.get_doc("Galaxy AI Agent", agent_name)  # existence check
    raise NotImplementedError(
        "Galaxy AI Agent runner is not yet implemented. See "
        "galaxy/ai_agents/runner.py for the planned design."
    )
