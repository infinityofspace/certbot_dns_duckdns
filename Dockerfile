FROM python:3.9-alpine3.13 as build-image

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /certbot_dns_duckdns

COPY build-requirements.txt build-requirements.txt
RUN pip install -r build-requirements.txt

COPY . .

RUN pip install .

FROM python:3.9-alpine3.13

COPY --from=build-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["certbot"]
