#!/bin/sh

echo "restarting ${CERTBOT_CONTAINER_NAME} container"
curl --unix-socket /var/run/docker.sock -X POST http:/v1.24/containers/${CERTBOT_CONTAINER_NAME}/restart
