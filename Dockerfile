FROM python:3.12-alpine3.19 AS build-image

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo

WORKDIR /certbot_dns_duckdns

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

FROM python:3.12-alpine3.19

COPY --from=build-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["certbot"]
