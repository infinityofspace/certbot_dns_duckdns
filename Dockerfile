FROM alpine:3.13

RUN apk update
RUN apk add --no-cache certbot python3 py3-pip

COPY . /certbot_dns_duckdns

WORKDIR /certbot_dns_duckdns

RUN pip install .

COPY scripts/ /scripts/
RUN chmod -R +x /scripts/

COPY cron/crontab /crontabs

ENV DEFAULT_LOG_FILE=/var/log/letsencrypt/certbot.log

ENTRYPOINT ["sh", "/scripts/certbot.sh"]
