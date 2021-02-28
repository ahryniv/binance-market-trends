from binance_market_trends.middlewares import catch_exceptions_middleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from binance_market_trends import __version__
from binance_market_trends.api import binance_market_trends_base
from binance_market_trends.conf.sentry import init_sentry
from binance_market_trends.conf.settings import settings, Env, Settings


def _init_middlewares(app: FastAPI, app_settings: Settings):
    app.middleware('http')(catch_exceptions_middleware)
    app.add_middleware(CORSMiddleware,
                       allow_origins=app_settings.ALLOWED_ORIGINS,
                       allow_credentials=True,
                       allow_methods=['*'],
                       allow_headers=["*"])


def create_app(app_settings: Settings = None):
    app_settings = app_settings if app_settings is not None else settings
    init_sentry(app_settings, version=__version__)
    is_production = app_settings.ENV == Env.PRODUCTION
    app = FastAPI(
        title='Binance Market Trends',
        description='Simple analyzer of Binance market',
        debug=app_settings.DEBUG,
        docs_url='/docs' if not is_production else None,
        redoc_url='/redoc' if not is_production else None,
        version=__version__,
    )
    _init_middlewares(app, app_settings)

    # routes
    app.include_router(binance_market_trends_base.router, tags=['Binance Market Trends'])
    return app
