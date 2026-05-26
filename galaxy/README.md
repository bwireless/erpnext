# Galaxy — eKosmos PSA

Galaxy is the eKosmos professional services automation (PSA) and MSP/MSSP
operations platform. It is delivered as a Frappe app that runs alongside
ERPNext, layering ticketing, SLAs, contracts, CMDB, knowledge base, client
portal, and AI agent management on top of ERPNext's accounting, CRM, and
project foundations.

Target deployment: `galaxy.ekosmos.com` on Azure.

## Status

This is the initial scaffold. It establishes:

- Frappe app skeleton (`hooks.py`, `modules.txt`, `pyproject.toml`)
- Branding override (logo, navbar, color tokens) that re-skins the Desk
- DocType stubs for the priority PSA modules:
  - Service Desk (Ticket, SLA Policy, Ticket Queue)
  - Contracts (MSP Contract, Recurring Plan)
  - CMDB / Asset (Configuration Item, RMM Integration)
  - Knowledge Base (Article, Category)
  - Client Portal (Settings)
  - AI Agents (Agent, Tool, Run, Message)

Each DocType is intentionally minimal — fields are in place so records can
be created and queried, but business logic (SLA timers, billing, RMM
sync, agent execution) is not yet wired. See `ROADMAP.md` (TBD) for the
phased build-out.

## Install (developer)

```bash
bench get-app galaxy /path/to/this/galaxy
bench --site galaxy.ekosmos.com install-app galaxy
bench --site galaxy.ekosmos.com migrate
bench build --app galaxy
```

## Brand

Placeholder palette and wordmark are committed under `galaxy/public/`.
See `BRAND.md` for the tokens and instructions for swapping in the real
ekosmos.com assets — the upstream site was unreachable when this scaffold
was generated, so the values here are intentional placeholders.
