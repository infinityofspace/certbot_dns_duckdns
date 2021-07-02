FROM alpine:3.14

RUN apk add --no-cache python3 py3-pip py3-cryptography

WORKDIR /certbot_dns_duckdns

COPY docker-build-requirements.txt docker-build-requirements.txt
RUN pip install -r docker-build-requirements.txt

COPY . .

RUN pip install .

ENTRYPOINT ["certbot"]
