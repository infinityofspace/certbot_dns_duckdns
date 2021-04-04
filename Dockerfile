FROM alpine:3.13

RUN apk update
RUN apk add --no-cache python3 py3-pip py3-cryptography
RUN pip install certbot certbot_dns_porkbun

COPY . /certbot_dns_duckdns

WORKDIR /certbot_dns_duckdns

RUN pip install .
