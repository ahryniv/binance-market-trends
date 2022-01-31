from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from binance_market_trends.services import MetricsService

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
async def test():
    """Make Some test"""
