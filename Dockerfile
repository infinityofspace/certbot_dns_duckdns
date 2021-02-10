FROM certbot/certbot:v1.12.0

WORKDIR /

COPY . /certbot_dns_duckdns

RUN pip install /certbot_dns_duckdns

COPY scripts/ /scripts/
RUN chmod -R +x /scripts/

COPY cron/crontab /crontabs

ENV DEFAULT_LOG_FILE=/var/log/letsencrypt/certbot.log

ENTRYPOINT ["sh", "/scripts/startup.sh"]
