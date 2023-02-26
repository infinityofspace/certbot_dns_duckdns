FROM python:3.11-alpine3.17 AS build-image

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo git \
     && if [[ $(uname -m) == armv6* ||  $(uname -m) == armv7* ]]; then \
          mkdir -p ~/.cargo/registry/index \
          && cd ~/.cargo/registry/index \
          && git clone --bare https://github.com/rust-lang/crates.io-index.git github.com-1285ae84e5963aae; \
        fi
        # workaround for cryptography arm build issue: see https://github.com/pyca/cryptography/issues/6673

WORKDIR /certbot_dns_duckdns

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

FROM python:3.11-alpine3.17

COPY --from=build-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["certbot"]
