# Galaxy PSA

**Galaxy** is an AI-first Professional Services Automation (PSA) and MSP/MSSP
operating system by **eKosmos Inc.**, built on top of the Frappe framework
and ERPNext.

Galaxy extends ERPNext with the full workflow surface an MSP needs:

| Area | Modules |
|------|---------|
| Service Desk | `PSA Ticket`, `SLA Policy`, `PSA Ticket Priority` |
| Contracts & Billing | `Service Contract`, `Retainer Block` |
| Assets / CMDB | `Configuration Item` |
| Projects & Time | `PSA Project Template`, `PSA Time Entry` |
| Quoting / CPQ | `PSA Quote` |
| Client Portal | `Client Portal Settings` (Single) |
| AI | `AI Runbook`, `AI Triage Rule` (Claude API) |
| Compliance (MSSP) | `Compliance Framework`, `Compliance Control` |

## Deployment

Galaxy runs as a Frappe bench app alongside ERPNext. For a single-VM
Docker Compose deployment on Azure (target: `galaxy.ekosmos.com`), see
[`../deploy/README.md`](../deploy/README.md).

## Branding

Galaxy ships eKosmos brand tokens (deep-space navy `#0B1026`, electron
purple `#7B5CFF`, supernova cyan `#37E2D5`) via CSS custom properties in
`galaxy_psa/public/css/galaxy_brand.css`. Replace the placeholder logo
at `galaxy_psa/public/images/galaxy-logo.svg` with the final eKosmos
asset when available.

## Bench install

```bash
bench get-app galaxy_psa /path/to/this/directory
bench --site galaxy.ekosmos.com install-app galaxy_psa
bench --site galaxy.ekosmos.com migrate
```
