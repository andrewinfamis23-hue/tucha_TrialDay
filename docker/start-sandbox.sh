#!/usr/bin/env bash
set -euo pipefail

DB_NAME="${DB_NAME:-tucha_sandbox}"

odoo --config=/etc/odoo/odoo.conf \
  --database="$DB_NAME" \
  --init=tucha_crm \
  --stop-after-init \
  --no-http

exec odoo --config=/etc/odoo/odoo.conf --database="$DB_NAME"
