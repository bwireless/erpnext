"""AI ticket triage via the Anthropic Claude API.

Invoked every 5 minutes by scheduler_events.

Environment:
    GALAXY_ANTHROPIC_API_KEY  — API key
    GALAXY_ANTHROPIC_MODEL    — model id (default: claude-sonnet-5)

This is a first-pass stub. It:
  1. finds unclassified PSA Tickets,
  2. asks Claude to summarize, categorize, suggest a reply,
  3. applies matching AI Triage Rules.
"""

from __future__ import annotations

import json
import os

import frappe

TRIAGE_SYSTEM_PROMPT = """You triage MSP support tickets for eKosmos.
Return a single JSON object with keys:
  summary       : 2-sentence summary
  category      : one of [Password, Hardware, Software, Network, Security,
                  Access, Backup, M365, Google Workspace, Billing, Other]
  suggested_reply : friendly, technically-accurate reply the tech can send
  confidence    : 0.0-1.0
Do not include any prose outside the JSON.
"""


def run_pending_triage(limit: int = 25):
	tickets = frappe.get_all(
		"PSA Ticket",
		filters={"ai_category": ["is", "not set"], "status": ["!=", "Closed"]},
		fields=["name", "subject", "description", "channel"],
		limit=limit,
	)
	for t in tickets:
		try:
			result = _triage_one(t)
		except Exception:
			frappe.log_error(frappe.get_traceback(), f"Galaxy AI triage failed for {t.name}")
			continue
		doc = frappe.get_doc("PSA Ticket", t.name)
		doc.ai_summary = result.get("summary")
		doc.ai_category = result.get("category")
		doc.ai_suggested_reply = result.get("suggested_reply")
		doc.ai_confidence = float(result.get("confidence") or 0)
		doc.save(ignore_permissions=True)


def _triage_one(ticket_row) -> dict:
	try:
		import anthropic
	except ImportError:
		raise RuntimeError("anthropic SDK not installed — pip install anthropic")

	api_key = os.getenv("GALAXY_ANTHROPIC_API_KEY") or frappe.conf.get("galaxy_anthropic_api_key")
	if not api_key:
		raise RuntimeError("GALAXY_ANTHROPIC_API_KEY not configured")

	model = os.getenv("GALAXY_ANTHROPIC_MODEL") or frappe.conf.get("galaxy_anthropic_model") or "claude-sonnet-5"
	client = anthropic.Anthropic(api_key=api_key)
	message = client.messages.create(
		model=model,
		max_tokens=1024,
		system=TRIAGE_SYSTEM_PROMPT,
		messages=[
			{
				"role": "user",
				"content": (
					f"Channel: {ticket_row.channel or 'Unknown'}\n"
					f"Subject: {ticket_row.subject}\n\n"
					f"Body:\n{ticket_row.description or ''}"
				),
			}
		],
	)
	# response is a list of content blocks; join text blocks
	text = "".join(block.text for block in message.content if getattr(block, "type", "") == "text")
	return json.loads(text)
