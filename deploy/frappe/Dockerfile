# Galaxy Frappe image — bakes Frappe + ERPNext + galaxy_psa into one bench.
#
# Multi-stage: the builder installs bench with all Python + Node deps,
# the runtime layer copies the assembled bench to a slim base.

ARG FRAPPE_BRANCH=version-15
ARG ERPNEXT_BRANCH=version-15
ARG PYTHON_VERSION=3.11.9
ARG NODE_VERSION=20.11.1

FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

ARG FRAPPE_BRANCH
ARG ERPNEXT_BRANCH
ARG NODE_VERSION
ENV DEBIAN_FRONTEND=noninteractive \
    NODE_VERSION=${NODE_VERSION} \
    NVM_DIR=/root/.nvm

RUN apt-get update && apt-get install --no-install-recommends -y \
        git build-essential curl ca-certificates gnupg wkhtmltopdf \
        libssl-dev libffi-dev libjpeg-dev libmariadb-dev \
        libpng-dev libwebp-dev libxml2-dev libxslt1-dev \
        cron redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Node via nvm (bench expects nvm-flavored node).
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
    && . "$NVM_DIR/nvm.sh" \
    && nvm install ${NODE_VERSION} \
    && nvm alias default ${NODE_VERSION}
ENV PATH="$NVM_DIR/versions/node/v${NODE_VERSION}/bin:$PATH"

RUN useradd --create-home --shell /bin/bash --uid 1000 frappe
USER frappe
WORKDIR /home/frappe

# Install bench, then initialize the bench dir.
RUN pip install --user frappe-bench
ENV PATH="/home/frappe/.local/bin:${PATH}"

RUN bench init --frappe-branch ${FRAPPE_BRANCH} --skip-redis-config-generation --skip-assets --python python3 frappe-bench
WORKDIR /home/frappe/frappe-bench

# Copy the local ERPNext fork (this repo's erpnext/ dir) and galaxy_psa
# into apps/. Build context is the repo root — see docker-compose.yml.
COPY --chown=frappe:frappe ./erpnext apps/erpnext
COPY --chown=frappe:frappe ./galaxy_psa apps/galaxy_psa

# Wire both apps into the bench so bench setup requirements picks them up.
RUN bench setup requirements \
    && echo -e "frappe\nerpnext\ngalaxy_psa" > sites/apps.txt

# Build frontend assets for all installed apps.
RUN bench build --production

# ---- Runtime -----------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim-bookworm AS runtime

ARG NODE_VERSION
ENV DEBIAN_FRONTEND=noninteractive \
    NODE_VERSION=${NODE_VERSION} \
    NVM_DIR=/root/.nvm \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
        git curl ca-certificates wkhtmltopdf libmariadb3 \
        libjpeg62-turbo libwebp7 libxml2 libxslt1.1 libpng16-16 \
        redis-tools mariadb-client \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash --uid 1000 frappe
USER frappe
WORKDIR /home/frappe

COPY --from=builder --chown=frappe:frappe /home/frappe/.local /home/frappe/.local
COPY --from=builder --chown=frappe:frappe /home/frappe/.nvm /home/frappe/.nvm
COPY --from=builder --chown=frappe:frappe /home/frappe/frappe-bench /home/frappe/frappe-bench

ENV PATH="/home/frappe/.local/bin:/home/frappe/.nvm/versions/node/v${NODE_VERSION}/bin:${PATH}"

WORKDIR /home/frappe/frappe-bench
COPY --chown=frappe:frappe ./deploy/frappe/entrypoint.sh /home/frappe/entrypoint.sh
RUN chmod +x /home/frappe/entrypoint.sh

EXPOSE 8000 9000
ENTRYPOINT ["/home/frappe/entrypoint.sh"]
CMD ["bench", "serve", "--port", "8000"]
