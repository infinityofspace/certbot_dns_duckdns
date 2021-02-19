#!/bin/bash

DOMAIN="${DOMAIN:-""}"
DUCKDNS_TOKEN="${DUCKDNS_TOKEN:-""}"
PROPAGATION_SECONDS="${PROPAGATION_SECONDS:-60}"
EMAIL="${EMAIL:-""}"
AUTORENEW="${AUTORENEW:-false}"
STAGING="${STAGING:-false}"
RECREATE="${RECREATE:-false}"
ADDITIONAL_CERTBOT_ARGS="${ADDITIONAL_CERTBOT_ARGS:-""}"

CERTBOT_COMMAND="certbot certonly --non-interactive --agree-tos --preferred-challenges dns --authenticator dns-duckdns"
LOG_FILE="/var/log/letsencrypt/certbot.log"

seven_days_s=$((60 * 60 * 24 * 7))

echo_and_log() {
  echo "$1" | tee -a "$LOG_FILE"
}

echo_and_log_err() {
  echo "$1" 2>&1 | tee -a "$LOG_FILE"
}

if [ "$RECREATE" = true ]; then
  echo "INFO: deleting all existing certificate data..."
  rm -rf /etc/letsencrypt
  rm -rf /var/log/letsencrypt
  echo "INFO: deleted all existing certificate data"
fi

mkdir -p "/var/log/letsencrypt/"

if [ "$DOMAIN" != "" ] && [ "$DUCKDNS_TOKEN" != "" ]; then
  # remove possible wildcard from domain
  domain_without_wildcard="${DOMAIN//\*./}"
  # check if a certificate already exists
  if [ -d "/etc/letsencrypt/live/$domain_without_wildcard" ]; then
    echo_and_log "INFO: found existing certificate"

    if ! openssl x509 -dates -noout -checkend $seven_days_s -in "/etc/letsencrypt/live/$domain_without_wildcard/cert.pem"; then
      echo_and_log "INFO: certificate ist too old and will be renewed"
      certbot renew
    else
      echo_and_log "INFO: existing certificate is valid and nothing will be changed"
    fi
  else
    # obtain a new certificate
    # prepare certbot arguments
    if [ "$EMAIL" == "" ]; then
      CERTBOT_COMMAND="$CERTBOT_COMMAND --register-unsafely-without-email"
    else
      CERTBOT_COMMAND="$CERTBOT_COMMAND --email \"$EMAIL\""
    fi

    CERTBOT_COMMAND="$CERTBOT_COMMAND --dns-duckdns-token \"$DUCKDNS_TOKEN\""
    CERTBOT_COMMAND="$CERTBOT_COMMAND --dns-duckdns-propagation-seconds $PROPAGATION_SECONDS"
    CERTBOT_COMMAND="$CERTBOT_COMMAND -d \"$DOMAIN\""
    CERTBOT_COMMAND="$CERTBOT_COMMAND $ADDITIONAL_CERTBOT_ARGS"

    if [ "$STAGING" = true ]; then
      echo_and_log "INFO: using staging environment"
      CERTBOT_COMMAND="$CERTBOT_COMMAND --staging"
    fi

    echo_and_log "INFO: obtaining a new certificate..."

    certbot_res=$(eval "$CERTBOT_COMMAND")
    echo_and_log "$certbot_res"
  fi
else
  echo_and_log_err "ERROR: domain or DuckDNS token not specified"
  exit 1
fi

if [ "$AUTORENEW" = true ]; then
  crontab /crontabs/crontab
  exec crond -f
fi

exit 0
