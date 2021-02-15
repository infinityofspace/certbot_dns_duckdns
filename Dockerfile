FROM alpine:3.13

RUN apk update
RUN apk add --no-cache certbot python3 py3-pip

WORKDIR /

COPY . /certbot_dns_duckdns

RUN pip install /certbot_dns_duckdns

COPY scripts/ /scripts/
RUN chmod -R +x /scripts/

COPY cron/crontab /crontabs

ENV DEFAULT_LOG_FILE=/var/log/letsencrypt/certbot.log

ENTRYPOINT ["sh", "/scripts/certbot.sh"]
