#!/bin/sh

crontab /crontabs/crontab
echo "starting cron daemon"
crond -f
