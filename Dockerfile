FROM python:3.9-slim-buster as base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.10 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

RUN apt-get update && apt-get install -y git gcc libpq-dev -y

RUN pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY binance_market_trends/ ./binance_market_trends

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-ansi


FROM python:3.9-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80
RUN apt-get update && apt-get install libpq-dev -y --no-install-recommends \
       && rm -rf /var/lib/apt/lists/*

COPY --from=base /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /app/binance_market_trends.egg-info/ /app/binance_market_trends.egg-info/

WORKDIR /app

COPY binance_market_trends/ ./binance_market_trends
COPY server.py/ ./server.py
COPY run_scrapers.py/ ./run_scrapers.py
COPY server-entrypoint.sh/ ./server-entrypoint.sh
COPY scraper-entrypoint.sh/ ./scraper-entrypoint.sh
COPY gunicorn-conf.py/ ./gunicorn-conf.py
COPY alembic.ini/ ./alembic.ini
COPY migrate_db.py/ ./migrate_db.py

CMD ["sh", "server-entrypoint.sh"]
