FROM alpine:3.16

RUN apk add --no-cache python3 py3-pip py3-cryptography

WORKDIR /certbot_dns_duckdns

COPY requirements-docker.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir .

ENTRYPOINT ["certbot"]
