from datetime import timedelta

from fastapi import APIRouter, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from binance_market_trends.services import MetricsService, RedditService

router = APIRouter()


@router.get(
    '/metrics',
    summary='Prometheus Metrics'
)
async def metrics() -> Response:
    """Endpoint for the Prometheus server with metrics"""
    await MetricsService().update_metrics()
    data = generate_latest()
    return Response(
        content=data,
        media_type=CONTENT_TYPE_LATEST,
    )


@router.get(
    '/test',
    summary='Test',
)
async def test(request: Request):
    """Make Some test"""
    app = request.app

    metric = app.state.metrics[PrometheusMetric.BINANCE_GROWING_SYMBOLS_TOTAL]

    # posts_count = await RedditService.get_last_posts_count(last=timedelta(minutes=5))
    # posts_count
