# Galaxy — Roadmap

This scaffold (slice 1) establishes the app skeleton, branding, and the
DocType surface area for the priority PSA modules. Subsequent slices
turn the surface area into working features.

## Slice 1 — Scaffold + Rebrand  (this commit)

- `galaxy` Frappe app with `hooks.py`, `modules.txt`, `pyproject.toml`
- Brand tokens, placeholder logo + favicon, Desk re-skin SCSS
- DocType stubs:
  - Service Desk: Galaxy Ticket, Galaxy SLA Policy, Galaxy SLA Target,
    Galaxy Ticket Queue, Galaxy Ticket Comment
  - Contracts: Galaxy MSP Contract, Galaxy Contract Line,
    Galaxy Recurring Invoice Plan
  - CMDB: Galaxy Configuration Item, Galaxy CI Relationship,
    Galaxy RMM Integration
  - Knowledge Base: Galaxy KB Article, Galaxy KB Category
  - Client Portal: Galaxy Portal Settings
  - AI Agents: Galaxy AI Agent, Galaxy AI Agent Tool,
    Galaxy AI Agent Run, Galaxy AI Agent Message
- App-screen entry, permission gate stub, branding hooks

## Slice 2 — Service Desk MVP

- SLA timer hook (hourly scheduler) that recomputes `sla_status` and
  emits "at risk" / "breached" events
- Ticket assignment + round-robin per queue
- Inbound email → Galaxy Ticket via Frappe Email Account
- Workspace + dashboard with ticket counts and SLA heat map

## Slice 3 — Contracts & Billing

- Recurring invoice generator that posts ERPNext Sales Invoices from
  Galaxy Recurring Invoice Plan on `daily` scheduler
- Prepaid-hours ledger linked to Timesheet
- Per-contract margin report

## Slice 4 — CMDB + RMM sync

- Concrete adapters for NinjaOne and Datto RMM (`galaxy/cmdb/rmm/`)
- Per-integration sync job; CI auto-creation on first-seen
- CI ↔ Ticket auto-link based on hostname/serial extraction

## Slice 5 — Client Portal

- Portal pages under `galaxy/www/portal/` for ticket submit/view, KB
  search, invoice list
- Optional AI intake (calls AI Agent flagged in Portal Settings)

## Slice 6 — AI Agents runtime

- Implement `galaxy/ai_agents/runner.py` against the Anthropic SDK
  (Opus 4.7 default), with Azure OpenAI / OpenAI optional providers
- Tool dispatch (`tools.py`) for `frappe_query`, `frappe_write`,
  `http_*`, `kb_search`, `rmm_action`
- Prompt caching on system blocks > 1024 tokens
- Trigger registry: DocEvent wiring, scheduler wiring, webhook endpoint
- Cost/usage rollups onto Galaxy AI Agent

## Slice 7 — Azure deployment

- Dockerfile for the bench (frappe + erpnext + galaxy + payments)
- Bicep / Terraform for: Azure Container Apps (web + worker),
  Azure Database for MariaDB, Azure Cache for Redis, Azure Blob for
  files, Front Door + custom domain for `galaxy.ekosmos.com`,
  Key Vault for secrets
- GitHub Actions: build, push to ACR, deploy
- Backup + restore runbook

## Out of scope (call out if you want them moved in)

- Mobile app
- Email marketing
- Project management beyond what ERPNext Projects already provides
- HR / payroll (use ERPNext HR if needed)
