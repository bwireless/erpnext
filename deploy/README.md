# Galaxy PSA — Azure Single-VM Deployment

This directory contains everything needed to run **galaxy.ekosmos.com**
on a single Azure VM using Docker Compose. Suitable for a pilot / MVP.
For production multi-tenant, migrate to AKS + the frappe/erpnext Helm
chart (a future PR will add that path).

## What you get

- **Frappe** + **ERPNext** + **galaxy_psa** custom app, all built into one
  image (`galaxy-frappe`).
- **MariaDB 10.11** for the site database.
- **Redis** for cache + queue + socketio.
- **Traefik** as reverse proxy — provisions a Let's Encrypt cert for
  `galaxy.ekosmos.com` automatically.
- **Frappe worker + scheduler + socketio + nginx** as separate services,
  matching the frappe_docker layout.

## Prerequisites

- An Azure VM (Ubuntu 24.04 LTS recommended)
  - Sizing for pilot: **Standard_D4as_v5** (4 vCPU, 16 GiB) — good for
    up to ~50 users
  - Data disk: 128 GiB Premium SSD for `/var/lib/docker`
- DNS: `galaxy.ekosmos.com` A-record pointing to the VM's public IP
- Ports **80** and **443** open in the NSG (Traefik terminates TLS)
- Ports 22 restricted to your admin CIDR
- An Anthropic API key for the AI triage (optional)

## First-time setup

1. Provision the VM. Attach it to your VNet. Assign a static public IP.
   Cloud-init `cloud-init.yaml` in this directory installs Docker and
   clones the repo — attach it as `custom-data` at VM create time.

2. SSH in and enter this directory:

   ```bash
   cd ~/galaxy/deploy
   cp env.example .env
   $EDITOR .env
   ```

   At minimum you MUST set:
   - `GALAXY_SITE_NAME` → `galaxy.ekosmos.com`
   - `GALAXY_ADMIN_PASSWORD` → strong password
   - `MARIADB_ROOT_PASSWORD` → strong password
   - `LETSENCRYPT_EMAIL` → an ops mailbox
   - `GALAXY_ANTHROPIC_API_KEY` → your Anthropic key (or leave blank to
     disable AI triage)

3. Build the image and bring the stack up:

   ```bash
   docker compose build
   docker compose up -d
   ```

4. Bootstrap the site (first time only):

   ```bash
   docker compose exec backend bench new-site "$GALAXY_SITE_NAME" \
       --mariadb-root-password "$MARIADB_ROOT_PASSWORD" \
       --admin-password "$GALAXY_ADMIN_PASSWORD" \
       --install-app erpnext \
       --install-app galaxy_psa
   docker compose exec backend bench --site "$GALAXY_SITE_NAME" migrate
   docker compose restart backend queue-long queue-short scheduler
   ```

5. Point a browser at **https://galaxy.ekosmos.com** — you should see
   the Galaxy branded login page.

## Day-2 operations

- **Update the app**: `git pull && docker compose build && docker compose up -d`
- **Bench console**: `docker compose exec backend bench --site $GALAXY_SITE_NAME console`
- **Logs**: `docker compose logs -f backend`
- **Backups** run nightly via the scheduler; database dumps land in the
  `sites/` volume under `<site>/private/backups/`. Rsync those to
  Azure Blob (a dedicated `backup` sidecar is future work).

## What's NOT in this pilot deployment

The single-VM setup is intentionally minimal. Missing for production:

- HA / no shared MariaDB (use Azure Database for MariaDB Flexible Server)
- Managed Redis (use Azure Cache for Redis)
- Object storage backups (use Azure Blob + `az storage blob upload-batch`)
- WAF / Front Door (put Azure Front Door Standard in front)
- Multi-tenant DNS + wildcard cert (needed if you host client sites)

## Files in this directory

| File | Purpose |
|---|---|
| `docker-compose.yml` | Service graph. |
| `frappe/Dockerfile` | Builds the Galaxy Frappe image (frappe + erpnext + galaxy_psa). |
| `frappe/entrypoint.sh` | Ensures site config points at containerized DB/Redis. |
| `traefik/traefik.yml` | Traefik static config — Let's Encrypt for galaxy.ekosmos.com. |
| `cloud-init.yaml` | First-boot VM setup — installs Docker, clones repo. |
| `env.example` | All required env vars, documented. |
