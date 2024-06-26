FROM python:3.12-bookworm AS dev

RUN python3 -m pip install poetry

WORKDIR /app

COPY . /app

RUN make debian

FROM bitnami/minideb:bookworm AS prod

RUN apt-get update

COPY --from=dev /app/dist/*.deb .

RUN if [ -f ./*-signed.deb ]; then \
        apt-get install -y --no-install-recommends ./*-signed.deb; \
    else \
        apt-get install -y --no-install-recommends ./*.deb; \
    fi && \
    rm -rf *.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

FROM prod AS validatornode01

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python", "-c", 'import requests; response = requests.get("http://localhost:8080/health/live"); response.raise_for_status();' ]

ENTRYPOINT bash -c 'source /opt/pantos/validator-node/virtual-environment/bin/activate && \
    exec mod_wsgi-express start-server \
    /opt/pantos/validator-node/wsgi.py \
    --user pantos-validator-node \
    --group pantos-validator-node \
    --port 8080 \
    --log-to-terminal \
    --error-log-format "%M"'

FROM prod AS validatornode01-celery-worker

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "bash", "-c", 'celery inspect ping -A pantos.validatornode -d celery@\$HOSTNAME' ]

ENTRYPOINT bash -c 'source /opt/pantos/validator-node/virtual-environment/bin/activate && \
    celery \
    -A pantos.validatornode \
    worker \
    --uid $(id -u pantos-validator-node) \
    --gid $(id -g pantos-validator-node) \
    -l INFO \
    --concurrency 4 \
    -n pantos.validatornode \
    -Q pantos.validatornode'
