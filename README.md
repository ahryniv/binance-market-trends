# Binance Market Trends #

![Python](https://img.shields.io/badge/python-v3.9-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-blue)

Simple analyzer of Binance market

## Prerequisites


## Set up
#### 1. Install dependencies

    $ poetry install && poetry shell

#### 2. Set environment variables

Look into `Environment variables` block in the bottom. 

#### 3. Run app

    $ python server.py

## Environment variables
| Variable                   | Description                                          | Default          |
|----------------------------|------------------------------------------------------|------------------|
| DEBUG                      | Debug mode                                           | False            |
| ENV                        | Environment [LOCAL, STAGING, PRODUCTION]             | LOCAL            |
| LOG_LEVEL                  | Log level [DEBUG, INFO, WARNING, ERROR, CRITICAL]    | INFO             |
| ALLOWED_ORIGINS            | Origins to allow requests from  (separated by space) | http://localhost |
| API_PORT                   | Port                                                 | 80               |
| SENTRY_DSN                 | DSN for the Sentry                                   | -                |
| POSTGRES_USER              | Username for DB connection                           | postgres         |
| POSTGRES_PASSWORD          | Password for DB connection                           | ""               |
| POSTGRES_HOSTNAME          | Hostname for DB connection                           | localhost        |
| POSTGRES_PORT              | Port for DB connection                               | 5432             |
| POSTGRES_DB                | DB name for DB connection                            | postgres         |
