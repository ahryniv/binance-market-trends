from prometheus_client import Gauge

from binance_market_trends.conf.constants import PrometheusMetric
from binance_market_trends.middlewares import catch_exceptions_middleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from binance_market_trends import __version__
from binance_market_trends.api import binance_market_trends_base, metrics
from binance_market_trends.conf.sentry import init_sentry
from binance_market_trends.conf.settings import settings, Env, Settings


def _init_middlewares(app: FastAPI, app_settings: Settings):
    app.middleware('http')(catch_exceptions_middleware)
    app.add_middleware(CORSMiddleware,
                       allow_origins=app_settings.ALLOWED_ORIGINS,
                       allow_credentials=True,
                       allow_methods=['*'],
                       allow_headers=["*"])


def _set_prometheus_metrics(app: FastAPI) -> None:
    """Set Prometheus Metrics"""
    app.state.metrics = {
        PrometheusMetric.BINANCE_BTC_TRADES: Gauge(
            PrometheusMetric.BINANCE_BTC_TRADES.lower(),
            'BTC Trades (FAKE)',
        ),
        PrometheusMetric.BINANCE_GROWING_SYMBOLS_USDT_TOTAL: Gauge(
            PrometheusMetric.BINANCE_GROWING_SYMBOLS_USDT_TOTAL.lower(),
            'Growing symbols to USDT in Binance market total',
        ),
        PrometheusMetric.BINANCE_FALLING_SYMBOLS_USDT_TOTAL: Gauge(
            PrometheusMetric.BINANCE_FALLING_SYMBOLS_USDT_TOTAL.lower(),
            'Falling symbols to USDT in Binance market total',
        ),
        PrometheusMetric.BINANCE_GROWING_SYMBOLS_USDT_PERCENT: Gauge(
            PrometheusMetric.BINANCE_GROWING_SYMBOLS_USDT_PERCENT.lower(),
            'Percent of Growing symbols to USDT in Binance market',
        ),
        PrometheusMetric.BINANCE_SAME_PRICE_SYMBOLS_USDT_TOTAL: Gauge(
            PrometheusMetric.BINANCE_SAME_PRICE_SYMBOLS_USDT_TOTAL.lower(),
            'Symbols with same price to USDT in Binance market total',
        ),
    }


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

    @app.on_event('startup')
    def startup() -> None:
        """Startup events"""
        _set_prometheus_metrics(app)

    # routes
    app.include_router(binance_market_trends_base.router, tags=['Binance Market Trends'])
    app.include_router(metrics.router, tags=['Prometheus Metrics'])
    return app
