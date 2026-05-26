# Galaxy PSA — Roadmap & Architecture

**Product:** Galaxy — eKosmos Inc.'s AI-first PSA / RMM / MSSP platform
**Domain:** `galaxy.ekosmos.com`
**Base:** ERPNext / Frappe Framework (custom app overlay)
**Target:** Single Azure VM running Docker Compose (pilot), with a documented path to Azure Container Apps and AKS as adoption grows.
**Benchmark:** HaloPSA feature parity, then exceed via AI-native workflows.

> Status: planning document. No application code has been written yet. This roadmap defines what we will build, in what order, and on what infrastructure.

---

## 1. Vision

Galaxy is the operating system for an AI-first MSP/MSSP. It unifies the workflows an MSP touches daily — ticketing, assets, contracts, projects, billing, security operations — and treats AI as a first-class teammate, not a chatbot bolted onto a legacy PSA.

Three differentiators we will not compromise on:

1. **AI-native every screen.** Every list view has a "ask Galaxy" pane. Every ticket has draft-reply, summarize-thread, suggest-next-action, propose-root-cause. Every customer has a generated executive briefing. Every contract has a renewal-risk score.
2. **MSSP-grade by default.** SOC views, alert triage, evidence collection, compliance reporting (CIS, SOC 2, HIPAA, PCI, NIST CSF, CMMC), and tenant isolation are core, not a paid module.
3. **One pane, one bill.** Tickets, time, assets, projects, expenses, recurring contracts, usage-based billing, and proposals all roll into a single invoice run — no integration tax.

---

## 2. Brand Identity

> ⚠️ `ekosmos.com` returned HTTP 403 to the harness fetcher (bot protection). The tokens below are **provisional**. Replace before code is written. Easiest path: paste the brand guide, or upload the logo SVG and a screenshot of the homepage.

### 2.1 Working palette (placeholder — needs confirmation)

| Token | Hex | Usage |
|---|---|---|
| `--galaxy-primary` | `#0B1E3F` | Deep space navy — chrome, headers |
| `--galaxy-accent` | `#5B8DEF` | Galaxy blue — primary CTAs, links |
| `--galaxy-nebula` | `#7B5BEF` | Violet accent — AI-generated UI, badges |
| `--galaxy-signal` | `#22C55E` | Healthy / resolved / passing |
| `--galaxy-warn` | `#F59E0B` | SLA at risk, pending |
| `--galaxy-critical` | `#EF4444` | SLA breach, P1, security alert |
| `--galaxy-surface` | `#0F172A` (dark) / `#FFFFFF` (light) | App background |
| `--galaxy-ink` | `#E2E8F0` (dark) / `#0B1E3F` (light) | Body text |

### 2.2 Typography (placeholder)

- **Display / brand:** Space Grotesk or Inter Tight
- **UI:** Inter
- **Mono:** JetBrains Mono (for logs, ticket IDs, asset serials)

### 2.3 Logo assets needed

- `galaxy-mark.svg` (icon-only, square, works at 24px favicon and 256px login)
- `galaxy-wordmark-light.svg` and `galaxy-wordmark-dark.svg`
- `galaxy-loader.svg` (animated mark for splash + AI thinking states)
- `favicon-32.png`, `favicon-180.png` (Apple touch), `og-image-1200x630.png`

### 2.4 Tone

Technical, calm, expert. Sentence case, no exclamation marks. AI suggestions are always labeled "Galaxy suggests" — never anthropomorphized as "I".

---

## 3. Architecture

### 3.1 Repo & app layout (custom-app overlay)

```
ekosmos/                            (new top-level git repo, or this one renamed)
├── apps/
│   ├── frappe/                     (upstream Frappe — pinned, untouched)
│   ├── erpnext/                    (this repo — pinned, untouched)
│   └── galaxy/                     (NEW — all our code lives here)
│       └── galaxy/
│           ├── hooks.py            (overrides: app_logo_url, splash, app_name "Galaxy")
│           ├── public/
│           │   ├── scss/galaxy.scss            (CSS-variable theme)
│           │   ├── js/galaxy_desk.bundle.js    (desk overrides)
│           │   └── images/                     (logo, favicon, og)
│           ├── psa/                (Ticket, SLA, Asset, Contract — see §4)
│           ├── rmm/                (Endpoint, Probe, Patch Policy)
│           ├── mssp/               (Alert, Incident, Evidence, Compliance)
│           ├── ai/                 (LLM gateway, prompts, agents, embeddings)
│           ├── billing/            (Recurring Contract, Usage Meter)
│           ├── portal/             (customer & technician portals)
│           └── integrations/       (M365, Intune, ConnectWise import, etc.)
└── deploy/
    ├── docker/                     (Dockerfile.galaxy + compose)
    ├── azure/                      (Bicep + cloud-init for the VM)
    └── ops/                        (backup, restore, runbooks)
```

**Rule:** never modify files inside `apps/frappe/` or `apps/erpnext/`. All changes are doctype overrides, fixtures, JS client scripts, or new doctypes in `apps/galaxy/`. This keeps `bench update` viable forever.

### 3.2 Runtime stack (pilot — Single Azure VM)

```
┌──────────────────────────────────────────────────────────┐
│ Azure VM (Standard D4s v5, 4 vCPU / 16 GiB / Premium SSD)│
│  Ubuntu 24.04 LTS                                        │
│  Docker Engine + Compose v2                              │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Caddy    │→ │ frappe   │  │ frappe   │  │ socketio │ │
│  │ (TLS,    │  │ web      │  │ worker   │  │ (realtime│ │
│  │  HTTP/3) │  │ x2       │  │ x3       │  │  + AI    │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │  stream) │ │
│       │             │             │        └──────────┘ │
│       ▼             ▼             ▼                     │
│  ┌─────────────────────────────────────────────────┐    │
│  │ MariaDB 10.6  │  Redis (cache+queue+socketio)   │    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
│  Volumes: /sites, /db, /redis, /logs (Premium SSD)       │
└──────────────────────────────────────────────────────────┘

External:
  • Azure DNS         → galaxy.ekosmos.com → VM public IP
  • Azure Blob (cool) → nightly site_config + DB dumps + assets snapshots
  • Azure Key Vault   → API keys (LLM provider, M365, Intune, etc.)
  • Azure Monitor     → metrics, log analytics workspace
  • Defender for      → VM + container runtime protection
    Cloud
```

Sizing rationale: 16 GiB RAM comfortably runs Frappe web×2 + worker×3 + MariaDB + Redis for ~50 concurrent users / 5k tickets/month. We'll instrument from day one so we know exactly when to scale.

### 3.3 When we outgrow single-VM

Pre-defined migration trigger: any of —
- p95 web latency > 800 ms for 7 consecutive days,
- > 75% sustained CPU for 7 days,
- > 50 concurrent active users,
- multi-region requirement appears.

Migration target: **Azure Container Apps** with MariaDB → Azure Database for MySQL Flexible Server, Redis → Azure Cache for Redis, Blob already external. AKS only if we hit multi-tenant white-label.

### 3.4 Backup & DR

- MariaDB `mariabackup` nightly → encrypted upload to Blob (cool tier), 30-day retention; weekly to archive tier, 1-year retention.
- `bench backup --with-files` weekly as belt-and-braces.
- VM-level Azure Backup daily snapshot, 14-day retention.
- Documented restore drill quarterly with RPO ≤ 24 h, RTO ≤ 4 h targets.

### 3.5 Security baseline

- TLS 1.3 only, HSTS preload, HTTP/3 via Caddy.
- SSH disabled by default; access via Azure Bastion only.
- Frappe admin behind WebAuthn (mandatory for any role containing "Admin").
- Per-doctype permission lock-down audit before go-live.
- All AI traffic routed through internal LLM gateway with PII scrubbing + audit log.
- Secrets only in Key Vault, mounted as env at container start, never in compose files.

---

## 4. Feature Inventory — HaloPSA Parity Matrix

Legend: ✅ exists in ERPNext, can be extended | 🟡 partial, needs work | 🆕 new doctype/module in `galaxy` app.

### 4.1 Service Desk

| Capability | ERPNext base | Galaxy plan |
|---|---|---|
| Tickets / Incidents | ✅ `Issue` | Extend → `Ticket` with type (Incident/Request/Problem/Change), impact×urgency matrix, parent/child linking, merge, split |
| SLA & OLA | ✅ `Service Level Agreement` | Add: business calendars per customer, holiday overrides, escalation chains, pause reasons, breach forecasting |
| Approvals | 🟡 Workflow | 🆕 `Change Approval Board`, CAB calendar, risk scoring |
| Major incident war room | 🟡 | 🆕 `Major Incident` with Teams bridge, status page push, comms templates |
| Problem mgmt (ITIL) | 🟡 | 🆕 `Problem` linking N incidents, known error DB |
| Knowledge base | 🟡 `Help Article` | Rebuild as `KB Article` with versioning, AI-suggested-from-ticket, public/private/per-customer scope |
| Self-service portal | 🟡 | 🆕 `Portal v2`: customer-branded, ticket submit, KB search, asset view, invoice pay, CSAT, status page |
| CSAT / NPS | 🆕 | `CSAT Survey` sent on resolve, NPS quarterly, dashboards |

### 4.2 Asset & Configuration Management (CMDB)

| Capability | Base | Plan |
|---|---|---|
| Assets | ✅ `Asset` (financial-leaning) | 🆕 parallel `Configuration Item` for IT assets — endpoint, server, network device, SaaS app, certificate, domain |
| Relationships | 🆕 | `CI Relationship` (depends-on, hosted-on, member-of) — service map graph |
| Software inventory | 🆕 | Auto-populated from Intune/Defender connector |
| Warranty / lifecycle | ✅ `Warranty Claim` | Extend with vendor portal links, end-of-life dashboards |
| Discovery | 🆕 | Agent or agentless probes; webhook ingest from Intune, Datto RMM, NinjaOne |

### 4.3 Projects & Professional Services

| Capability | Base | Plan |
|---|---|---|
| Projects, tasks, dependencies | ✅ | Extend with project templates per service offering |
| Gantt | ✅ | Replace with React-based interactive board |
| Resource planning | 🟡 | 🆕 `Resource Plan` — capacity per skill, utilization heatmap |
| Time tracking | ✅ `Timesheet` | Add timer widget in every ticket; auto-suggest activity from ticket subject |
| Project billing | ✅ | Wire to recurring + usage billing engine (§4.5) |

### 4.4 CRM / Sales

| Capability | Base | Plan |
|---|---|---|
| Leads, Opportunities, Quotations | ✅ | Keep, restyle |
| Proposals / SoW | 🟡 | 🆕 `Proposal` with template variables, e-sign (DocuSign/Dropbox Sign), versioning |
| Quote-to-contract automation | 🆕 | On Quote acceptance → spawn Recurring Contract + Project + onboarding tasks |

### 4.5 Contracts & Billing

| Capability | Base | Plan |
|---|---|---|
| Recurring invoicing | 🟡 `Subscription` | 🆕 `Recurring Contract` — per-seat, per-device, tiered, with proration |
| Usage-based billing | 🆕 | `Usage Meter` ingesting from M365 license API, Azure consumption, backup TB used |
| Block-hour / retainer | 🆕 | `Retainer` with rollover rules, low-balance alerts |
| Multi-currency | ✅ | Inherit |
| Stripe / ACH / wire | 🟡 | Add Stripe Billing Portal embed, Plaid ACH, wire instructions per currency |
| AR collections | 🆕 | Dunning ladder, AI-drafted dunning emails, customer credit hold |

### 4.6 RMM-light (Phase 3)

We will not build a full RMM agent. We **will** build:
- `Endpoint` CI synced from Intune + Defender + selected partners (NinjaOne, Datto, N-able).
- `Patch Policy` and `Patch Run` records pulled from Intune / WSUS reports.
- `Monitor Alert` ingest endpoint (webhook from PRTG, Datadog, Zabbix, Defender) → auto-create ticket per rules.

### 4.7 MSSP / Security Operations

| Capability | Plan |
|---|---|
| Alert ingestion | 🆕 `Security Alert` from Defender for Cloud, Sentinel, Huntress, Crowdstrike |
| Triage queue | 🆕 SOC dashboard, severity x asset criticality, AI auto-triage suggestion |
| Incident response | 🆕 `Security Incident` with playbook runner, evidence locker |
| Evidence collection | 🆕 immutable Blob (legal hold) per incident |
| Compliance frameworks | 🆕 `Compliance Control` mapped to CIS v8, SOC 2 CC, HIPAA, PCI DSS 4.0, NIST CSF 2.0, CMMC L2 |
| Customer-facing security score | 🆕 monthly automated report per customer with posture trend |
| Vulnerability mgmt | 🆕 ingest from Defender Vuln Mgmt, Qualys, Tenable; link to CIs |
| Phishing sim results | 🆕 ingest KnowBe4 / Hoxhunt |

### 4.8 AI Layer (Galaxy's differentiator)

- **LLM gateway** — single internal service, provider-agnostic, with PII scrubbing, per-tenant budget caps, full audit log.
- **Embeddings index** — every Ticket, KB Article, CI, Contract embedded for semantic search.
- **Agents (start narrow, expand):**
  - *Draft Reply* — context = ticket thread + customer history + KB hits.
  - *Triage* — assigns queue, priority, suggested assignee on ticket creation.
  - *Summarize* — thread, contract, customer-quarterly-review.
  - *Root Cause Hypothesizer* — for major incidents, links related CIs and recent changes.
  - *Renewal Risk* — scores each contract 0–100 with reason codes.
  - *QBR Builder* — generates per-customer quarterly review deck.
  - *Compliance Evidence Mapper* — proposes which Galaxy records satisfy which control.
- **"Ask Galaxy" omni-bar** — every page; scoped to current context (customer, ticket, project).

### 4.9 Integrations (priority order)

1. Microsoft 365 (Graph): users, mailboxes, license counts → usage meter; Teams ticket bot.
2. Microsoft Intune: endpoint CIs, patch state, compliance.
3. Microsoft Defender (Endpoint + Cloud) + Sentinel: alerts → tickets.
4. Azure Billing / Cost Management: customer subscription cost roll-up.
5. Stripe + Plaid: card + ACH.
6. DocuSign / Dropbox Sign: SoW e-sign.
7. Slack + Teams: notifications, slash commands, approvals.
8. Datto BCDR, Veeam: backup health → CI status.
9. ConnectWise + HaloPSA importers: ticket / customer / contract migration scripts.

---

## 5. Phased Delivery Plan

Estimates assume 2 senior full-stack engineers + 1 Frappe specialist + 0.5 designer. Adjust linearly.

### Phase 0 — Foundation (2 weeks)
- Provision Azure VM, DNS, TLS, backups, monitoring, Key Vault.
- Create `galaxy` custom app, override `app_name`, logo, splash, login page.
- Apply theme tokens (§2) as SCSS variables.
- CI/CD: GitHub Actions → SSH deploy to VM, blue/green by container relabel.
- Disable / hide modules we don't need (Manufacturing, Stock-heavy, Agriculture, Education, Healthcare, POS).
- **Exit:** `https://galaxy.ekosmos.com` shows branded login; engineers can `git push` → live in < 5 min.

### Phase 1 — Service Desk MVP (4 weeks)
- `Ticket` doctype (extends Issue), SLA v2, escalation chains, merge/split, parent/child.
- Customer portal v2 (ticket submit + view, KB search, CSAT).
- KB Article v2 with versioning.
- Email-to-ticket with threading + signature stripping.
- Basic dashboards: queue health, SLA risk, agent leaderboard.
- **Exit:** internal eKosmos team dogfoods Galaxy for our own tickets.

### Phase 2 — CMDB + Time + Billing core (5 weeks)
- `Configuration Item` + relationships + service map.
- M365 + Intune connectors → CI auto-sync.
- Ticket ⇄ CI linkage; impacted CI shown on every ticket.
- Timer in every ticket; weekly timesheet approval.
- `Recurring Contract` + first invoice run; Stripe live.
- **Exit:** one pilot customer fully billed through Galaxy.

### Phase 3 — Projects + Proposals + CRM (4 weeks)
- Project templates per service offering.
- Resource planning + utilization heatmap.
- `Proposal` with e-sign; quote-to-contract automation.
- Lead → Opportunity → Quote pipeline restyled.
- **Exit:** new customer can be sold + onboarded + billed end-to-end in Galaxy.

### Phase 4 — AI Layer v1 (4 weeks)
- LLM gateway service + audit log.
- Embeddings index (Ticket, KB, CI, Contract).
- Agents: Draft Reply, Triage, Summarize, Ask Galaxy omni-bar.
- Per-tenant budget caps + dashboards.
- **Exit:** 50% of ticket replies start as Galaxy drafts; measured deflection on portal.

### Phase 5 — MSSP module (6 weeks)
- `Security Alert` ingest (Defender, Sentinel, Huntress).
- `Security Incident` with playbook runner + evidence locker.
- Compliance Controls library + evidence mapping (CIS, SOC 2, HIPAA).
- Per-customer monthly security report (AI-drafted, human-signed).
- **Exit:** Galaxy is sellable as an MSSP product, not just MSP.

### Phase 6 — RMM-light + Advanced Billing (4 weeks)
- Monitor Alert webhook ingest.
- Patch policy / patch run records.
- Usage meter (M365 licenses, Azure cost, backup TB).
- Retainer / block-hour with rollover.
- Dunning automation.
- **Exit:** full HaloPSA functional parity claim defensible.

### Phase 7 — AI Layer v2 + Public launch (ongoing)
- Renewal risk, QBR builder, compliance mapper.
- Multi-tenant white-label option (triggers Container Apps / AKS migration).
- Marketplace for integrations.

**Total to functional parity:** ~29 engineer-weeks of focused work (≈ 7 calendar months at 2.5 FTE). AI differentiators land in parallel from Phase 4 onward.

---

## 6. Cost Estimate (pilot, monthly USD, Azure list pricing East US 2)

| Item | Spec | Est. /mo |
|---|---|---|
| VM Standard D4s v5 | 4 vCPU / 16 GiB | ~$140 |
| Premium SSD P10 ×2 (OS + data, 128 GiB each) | | ~$38 |
| Azure Backup (VM, 14 day) | ~50 GiB churn | ~$10 |
| Blob storage cool (DB dumps, 30 day) | ~50 GiB | ~$1 |
| Blob storage archive (yearly) | ~600 GiB | ~$2 |
| Azure DNS zone | | ~$0.50 |
| Public IP (static) | | ~$4 |
| Azure Bastion (Basic) | optional | ~$140 |
| Key Vault | low ops | ~$1 |
| Log Analytics workspace | ~5 GiB/day | ~$25 |
| Defender for Servers Plan 2 | per VM | ~$15 |
| **Subtotal infra** | | **~$235 ($375 with Bastion)** |
| LLM API (assume Claude / GPT, 2M tokens/day) | | ~$300–800 |
| Stripe + Plaid | per transaction | n/a until live |
| **Total pilot run-rate** | | **~$500–1,200/mo** |

This scales sub-linearly until the §3.3 migration triggers fire.

---

## 7. Risks & Open Questions

| # | Risk / Question | Mitigation / Need from you |
|---|---|---|
| R1 | ERPNext is GPLv3. A hosted SaaS is fine; redistributing Galaxy as a product means source disclosure of derivative parts. | Confirm we are SaaS-only, or budget for clean-room rewrite of public-facing surfaces. |
| R2 | Frappe upgrades break custom overrides. | Pin Frappe + ERPNext; quarterly upgrade window; integration test suite from day one. |
| R3 | Single VM = single point of failure. | RPO/RTO documented (§3.4). Pilot only. Migration trigger pre-defined (§3.3). |
| R4 | LLM PII leakage. | Gateway scrubs before send; audit log; per-tenant opt-out; consider Azure OpenAI for data-residency customers. |
| R5 | HaloPSA parity is a moving target. | Lock the §4 matrix as v1 scope; new features go in a backlog reviewed quarterly. |
| Q1 | Brand assets — need logo SVG + confirmed palette (see §2). | Upload or paste guide. |
| Q2 | Tenant model — single-tenant per customer instance, or multi-tenant from day one? | Recommend: single-tenant pilot, multi-tenant Phase 7. |
| Q3 | Which LLM provider for v1? Claude (Anthropic), Azure OpenAI, or both via gateway? | Recommend Azure OpenAI for residency + Claude for higher-quality drafts, both behind gateway. |
| Q4 | Migration data sources — are we importing from an existing PSA (HaloPSA, ConnectWise, Autotask)? | Affects Phase 0/1 scope. |
| Q5 | Region — East US 2 assumed; data residency requirements? | Affects Azure region + LLM choice. |

---

## 8. Next Session — Recommended Order

1. **Brand confirmation** — paste palette + upload logo SVG. (5 min of your time.)
2. **Phase 0 build** — scaffold `apps/galaxy/`, theme overrides, `deploy/docker/` + `deploy/azure/` Bicep + cloud-init, GitHub Actions deploy. End state: branded login page on a real VM at `galaxy.ekosmos.com`.
3. **Phase 1 sprint 1** — `Ticket` doctype with extended fields + SLA v2 schema.

Each is a discrete session. Phase 0 is roughly a full session of focused work.
