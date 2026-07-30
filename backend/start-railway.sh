#!/bin/sh
set -eu

: "${CF_ACCESS_HOSTNAME:?CF_ACCESS_HOSTNAME is missing}"
: "${TUNNEL_SERVICE_TOKEN_ID:?TUNNEL_SERVICE_TOKEN_ID is missing}"
: "${TUNNEL_SERVICE_TOKEN_SECRET:?TUNNEL_SERVICE_TOKEN_SECRET is missing}"
: "${DATABASE_URL:?DATABASE_URL is missing}"

echo "Starting Cloudflare PostgreSQL proxy..."

cloudflared access tcp \
  --hostname "$CF_ACCESS_HOSTNAME" \
  --url 127.0.0.1:15432 \
  --service-token-id "$TUNNEL_SERVICE_TOKEN_ID" \
  --service-token-secret "$TUNNEL_SERVICE_TOKEN_SECRET" \
  --loglevel info &

CLOUDFLARED_PID=$!

cleanup() {
  kill "$CLOUDFLARED_PID" 2>/dev/null || true
}

trap cleanup INT TERM EXIT

echo "Waiting for local PostgreSQL proxy..."

python - <<'PY'
import socket
import sys
import time

for attempt in range(60):
    try:
        with socket.create_connection(("127.0.0.1", 15432), timeout=1):
            print("Cloudflare PostgreSQL proxy is ready.")
            break
    except OSError:
        time.sleep(1)
else:
    print("Cloudflare PostgreSQL proxy did not become ready.", file=sys.stderr)
    sys.exit(1)
PY

exec python run.py