# Galaxy PSA — Roadmap

This document tracks what shipped in the initial `galaxy_psa` scaffold
and the ordered follow-up work to reach a HaloPSA-class product.

## Shipped in this branch (`claude/epic-newton-qHnFV`)

### `galaxy_psa/` — new Frappe app

- Standalone Frappe app: `setup.py`, `pyproject.toml`, `MANIFEST.in`,
  `hooks.py`, `modules.txt`, `boot.py`.
- Custom roles: Galaxy Technician, Dispatcher, Service Manager,
  Security Analyst, Client Contact.
- Brand-token CSS (`galaxy_brand.css`) + JS shim (`galaxy_desk.js`).
- Placeholder Galaxy wordmark SVG + favicon (cosmic dark theme).
- Desktop module cards for all 8 modules with themed colors + icons.

### DocTypes (13)

| Module | DocType | Purpose |
|---|---|---|
| Service Desk | `PSA Ticket` | Multi-channel tickets with SLA + AI triage fields |
| Service Desk | `SLA Policy` | Business-hours-aware response/resolution targets, escalation |
| Service Desk | `PSA Ticket Priority` | Weighted priority levels |
| Service Desk | `PSA Ticket Queue` | Named queues for routing |
| Contracts | `Service Contract` | MRR, billing cycle, included hours, SLA linkage |
| Contracts | `Retainer Block` | Purchased/consumed/remaining-hour burndown |
| Assets CMDB | `Configuration Item` | Full CI with RMM fields (NinjaOne/Datto/Auvik) |
| Projects Time | `PSA Project Template` | Reusable project outlines with JSON task tree |
| Projects Time | `PSA Time Entry` | Timer + burns retainer + rolls up to ticket on submit |
| CPQ | `PSA Quote` | Quote with approval + e-sign hooks (DocuSign/HelloSign/PandaDoc) |
| Client Portal | `Client Portal Settings` | Single doc, portal branding + feature flags |
| AI | `AI Runbook` | Human/AI-authored playbooks with trigger + steps |
| AI | `AI Triage Rule` | Route/prioritize/reply based on Claude classification |
| Compliance | `Compliance Framework` | SOC2/CIS/NIST/ISO27001/HIPAA/PCI-DSS |
| Compliance | `Compliance Control` | Individual control with evidence + review cadence |

### Scheduler hooks (stubs)

- `service_desk.sla.check_sla_breaches` — hourly
- `contracts.billing.generate_recurring_invoices` — daily
- `assets_cmdb.discovery.reconcile_rmm_inventory` — daily
- `ai.triage.run_pending_triage` — every 5 min (calls Claude API)

### Deployment (`deploy/`)

- Single-VM Docker Compose stack (frappe + workers + scheduler + socketio + traefik + mariadb + redis).
- Traefik with automatic Let's Encrypt for `galaxy.ekosmos.com`.
- Cloud-init for Ubuntu 24.04 Azure VMs (D4as_v5 recommended).
- `env.example` documenting every required var.
- Deployment README with bench bootstrap steps.

## Not yet shipped — ordered follow-ups

### Sprint 1 — Service Desk depth (2 weeks)

1. Ticket comments/threading with public/private note flag
2. Email inbox → ticket bridge (extending Frappe's Communication)
3. SLA `Holiday List` integration (dependency exists but unused)
4. Escalation execution — the SLA check job only publishes events today
5. Ticket merge, split, parent/child
6. Bulk actions (assign, close, priority) on list view

### Sprint 2 — Billing loop closes (2 weeks)

1. `Service Contract` → auto-create Sales Invoice via ERPNext Selling
2. `PSA Time Entry` bulk-invoice from approved unbilled entries
3. Retainer overage detection → invoice line with overage_rate
4. Recurring invoice cron actually creates invoices (currently stubbed)
5. Reports: WIP, aged AR, contract profitability

### Sprint 3 — Assets + RMM integrations (2 weeks)

1. NinjaOne API client — pull devices, alerts
2. Datto RMM API client
3. Auvik API client
4. `RMM Integration Settings` Single with keys per source
5. Alert → `PSA Ticket` auto-create rules

### Sprint 4 — Client Portal (2 weeks)

1. Portal home page (`www/portal.html`)
2. `/tickets` list + detail with reply thread
3. `/my-assets`, `/my-contracts`, `/invoices` views
4. KB with Frappe Wiki integration
5. Portal user provisioning from Customer Contact

### Sprint 5 — AI-first differentiators (2 weeks)

1. AI ticket triage — this scaffold has the pipe; wire real API keys
2. Suggested reply insertion in ticket UI (JS)
3. Weekly customer executive summary via Claude
4. Runbook auto-generation from resolved tickets
5. KB semantic search via embeddings

### Sprint 6 — MSSP / SOC (2 weeks)

1. SIEM alert ingestion (webhook endpoint)
2. Incident Response ticket type + IR runbook templates
3. Evidence attachment DocType linked to Compliance Control
4. Customer-facing compliance dashboard (per-framework % complete)
5. SOC2/CIS/NIST/ISO27001 seed data (framework + controls)

### Sprint 7 — CPQ / Sales (2 weeks)

1. `Vendor Catalog` DocType + Pax8/Ingram sync
2. Quote line items with configuration (child DocType)
3. E-sign integration (DocuSign first)
4. Opportunity pipeline board

### Post-pilot — Azure production hardening

1. Migrate to Azure Container Apps + MariaDB Flexible Server
2. AKS + Helm chart path for multi-tenant
3. Azure Blob backup sidecar
4. Front Door + WAF
5. Managed identity for Anthropic key rotation (Key Vault)

## References for feature completeness

- HaloPSA feature list — https://halopsa.com/features/
- ConnectWise Manage
- Autotask PSA
- SuperOps
- Syncro
