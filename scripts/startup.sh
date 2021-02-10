#!/bin/bash

sh ./scripts/certbot.sh

AUTORENEW="${AUTORENEW:-false}"

if [ "$AUTORENEW" = true ]; then
  crontab /crontabs/crontab
  exec crond -f
fi
