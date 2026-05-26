# Azure deployment — placeholder

Azure deployment is **slice 7** on the roadmap. This directory is a
placeholder so the layout is reserved and the next slice can drop in:

- `Dockerfile` — bench image with frappe + erpnext + galaxy
- `docker-compose.yml` — local stack (web, worker, mariadb, redis)
- `bicep/main.bicep` — Container Apps, MariaDB Flexible Server,
  Azure Cache for Redis, Storage Account, Front Door, Key Vault
- `github/workflows/deploy.yml` — CI: build → ACR push → revision deploy

Target hostname: `galaxy.ekosmos.com` (Front Door custom domain →
Container Apps environment).
