#!/bin/sh
# Runs inside a clean Python container. Installs the given certbot version together
# with this plugin and checks that the plugin is registered and certbot works.
#
# Usage: check_certbot_version.sh <certbot-version>
# Expects the plugin source mounted read-only at /src.
set -eu

CERTBOT_VERSION="$1"
WORK="$(mktemp -d)"
CB_DIRS="--config-dir $WORK/config --work-dir $WORK/work --logs-dir $WORK/logs"

step() { echo "==> $*"; }

step "python $(python --version 2>&1 | cut -d' ' -f2), certbot==$CERTBOT_VERSION"
cp -r /src "$WORK/src"
rm -rf "$WORK/src/venv" "$WORK/src/build" "$WORK/src"/*.egg-info

step "install certbot==$CERTBOT_VERSION + acme==$CERTBOT_VERSION + plugin"
# certbot < 2.x only requires acme>=<old>, so pip would pull the newest acme which
# breaks old certbot on its own. certbot and acme are always released in lockstep,
# so pin acme to the matching version.
pip install --quiet --disable-pip-version-check --root-user-action=ignore \
    "certbot==$CERTBOT_VERSION" "acme==$CERTBOT_VERSION" "$WORK/src" "responses"
pip list --disable-pip-version-check 2>/dev/null | grep -iE '^(certbot|acme|josepy|cryptography|pyopenssl|setuptools|dnspython|requests) '
# Make sure pip did not silently resolve a different certbot version.
INSTALLED="$(python -c 'import certbot; print(certbot.__version__)')"
[ "$INSTALLED" = "$CERTBOT_VERSION" ] || { echo "installed certbot $INSTALLED != $CERTBOT_VERSION"; exit 1; }

step "certbot --version"
certbot --version

step "plugin registered (certbot plugins)"
# shellcheck disable=SC2086
certbot plugins --text $CB_DIRS 2>&1 | tee "$WORK/plugins.txt"
grep -q "^\* dns-duckdns" "$WORK/plugins.txt"

step "plugin init + prepare"
# shellcheck disable=SC2086
certbot plugins --text --init --prepare --authenticators $CB_DIRS 2>&1 | tee "$WORK/prepare.txt"
grep -q "^\* dns-duckdns" "$WORK/prepare.txt"
grep -q "Initialized: <certbot_dns_duckdns.cert.client.Authenticator" "$WORK/prepare.txt"

step "plugin cli options (certbot --help dns-duckdns)"
# shellcheck disable=SC2086
certbot --help dns-duckdns $CB_DIRS > "$WORK/help.txt" 2>&1
for opt in --dns-duckdns-token --dns-duckdns-credentials --dns-duckdns-propagation-seconds --dns-duckdns-no-txt-restore; do
    grep -q -- "$opt" "$WORK/help.txt" || { cat "$WORK/help.txt"; echo "missing option $opt"; exit 1; }
done

step "unit tests"
cd "$WORK/src"
python -m unittest tests/*.py > "$WORK/unittest.txt" 2>&1 || { cat "$WORK/unittest.txt"; exit 1; }
tail -n 3 "$WORK/unittest.txt"

echo "RESULT: certbot $CERTBOT_VERSION OK"
