#!/usr/bin/env bash
# Entrypoint for Galaxy Frappe container.
#
# Ensures common_site_config.json points at containerized MariaDB and Redis
# before delegating to bench. Runs at every container start (idempotent).

set -euo pipefail

BENCH_DIR="/home/frappe/frappe-bench"
CONFIG="${BENCH_DIR}/sites/common_site_config.json"

cd "${BENCH_DIR}"

if [ ! -f "${CONFIG}" ]; then
    cat > "${CONFIG}" <<EOF
{
    "db_host": "mariadb",
    "db_port": 3306,
    "redis_cache": "redis://redis-cache:6379",
    "redis_queue": "redis://redis-queue:6379",
    "redis_socketio": "redis://redis-queue:6379",
    "socketio_port": 9000,
    "webserver_port": 8000,
    "developer_mode": 0,
    "serve_default_site": true,
    "default_site": "${GALAXY_SITE_NAME:-galaxy.ekosmos.com}",
    "galaxy_anthropic_api_key": "${GALAXY_ANTHROPIC_API_KEY:-}",
    "galaxy_anthropic_model": "${GALAXY_ANTHROPIC_MODEL:-claude-sonnet-5}"
}
EOF
fi

exec "$@"
