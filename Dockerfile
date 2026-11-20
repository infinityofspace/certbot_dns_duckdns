FROM python:3.15-alpine3.24 AS build-image

ARG TARGETARCH
ARG TARGETVARIANT

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo

WORKDIR /certbot_dns_duckdns

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN if [ "$TARGETARCH" = "arm" ] && [ "$TARGETVARIANT" = "v6" ]; then \
        export PIP_NO_BINARY=charset-normalizer; \
    fi; \
    pip install -r requirements.txt

COPY . .
RUN if [ "$TARGETARCH" = "arm" ] && [ "$TARGETVARIANT" = "v6" ]; then \
        export PIP_NO_BINARY=charset-normalizer; \
    fi; \
    pip install .

FROM python:3.15-alpine3.24

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY --from=build-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["./docker-entrypoint.sh"]
