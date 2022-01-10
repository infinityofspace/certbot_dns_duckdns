FROM alpine:3.14

RUN apk add --no-cache python3 py3-pip py3-cryptography

WORKDIR /certbot_dns_duckdns

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN pip install .

ENTRYPOINT ["certbot"]
