#!/bin/sh
# Tests which certbot versions work with this plugin, each in a fresh python container.
#
# Usage:
#   scripts/certbot_compat/test_certbot_versions.sh                # first release of every minor >= MIN_VERSION
#   scripts/certbot_compat/test_certbot_versions.sh 1.18.0 2.0.0   # explicit versions
#
# Env: PYTHON_IMAGE (default python:3.11-slim), MIN_VERSION (default 1.18.0)
set -eu

PYTHON_IMAGE="${PYTHON_IMAGE:-python:3.11-slim}"
MIN_VERSION="${MIN_VERSION:-1.18.0}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LOG_DIR="$ROOT/build/certbot_compat"
mkdir -p "$LOG_DIR"

if [ "$#" -gt 0 ]; then
    VERSIONS="$*"
else
    # Oldest release of each minor version >= MIN_VERSION, ascending.
    VERSIONS="$(curl -fsSL https://pypi.org/pypi/certbot/json | python3 -c '
import json, sys
min_v = tuple(map(int, sys.argv[1].split(".")))
rel = json.load(sys.stdin)["releases"]
vs = sorted(
    (tuple(map(int, v.split("."))) for v, files in rel.items()
     if files and all(p.isdigit() for p in v.split("."))),
)
seen = {}
for v in vs:
    if v >= min_v:
        seen.setdefault(v[:2], v)
print(" ".join(".".join(map(str, v)) for v in seen.values()))
' "$MIN_VERSION")"
fi

echo "Image: $PYTHON_IMAGE"
echo "Versions: $VERSIONS"
SUMMARY=""
for v in $VERSIONS; do
    printf '%-8s ... ' "$v"
    if docker run --rm \
        -v "$ROOT:/src:ro" \
        -v certbot-compat-pip-cache:/root/.cache/pip \
        "$PYTHON_IMAGE" sh /src/scripts/certbot_compat/check_certbot_version.sh "$v" \
        > "$LOG_DIR/certbot-$v.log" 2>&1; then
        echo "OK"; SUMMARY="$SUMMARY\n$v OK"
    else
        echo "FAIL (see $LOG_DIR/certbot-$v.log)"; SUMMARY="$SUMMARY\n$v FAIL"
    fi
done
printf "\nSummary:%b\n" "$SUMMARY" | tee "$LOG_DIR/summary.txt"
