from random import randint

from fastapi import APIRouter, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from binance_market_trends.clients import binance_client
from binance_market_trends.conf.constants import PrometheusMetric
from binance_market_trends.services.metrics_service import MetricsService

router = APIRouter()


@router.get(
    '/metrics',
    summary='Prometheus Metrics'
)
async def metrics(request: Request) -> Response:
    """Endpoint for the Prometheus server with metrics"""
    app = request.app
    prices_change = await MetricsService().prices_change()
    app.state.metrics[PrometheusMetric.BINANCE_BTC_TRADES].set(randint(1, 100))
    app.state.metrics[PrometheusMetric.BINANCE_GROWING_SYMBOLS_USDT_TOTAL].set(prices_change.growing)
    app.state.metrics[PrometheusMetric.BINANCE_FALLING_SYMBOLS_USDT_TOTAL].set(prices_change.falling)
    app.state.metrics[PrometheusMetric.BINANCE_GROWING_SYMBOLS_USDT_PERCENT].set(prices_change.growing_percent)
    app.state.metrics[PrometheusMetric.BINANCE_SAME_PRICE_SYMBOLS_USDT_TOTAL].set(prices_change.same_price)
    data = generate_latest()
    return Response(
        content=data,
        media_type=CONTENT_TYPE_LATEST,
    )


@router.get(
    '/test',
    summary='Test',
)
async def test():
    """Make Some test"""
    response = await MetricsService().prices_change()
    response
