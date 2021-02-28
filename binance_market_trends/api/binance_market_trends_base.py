from fastapi import APIRouter, Request

from binance_market_trends.schemas.ok import OKSchema
from binance_market_trends.schemas.version import VersionSchema

router = APIRouter()


@router.get(
    '/health',
    summary='Health check',
    response_model=OKSchema,
)
async def health():
    """Shows status of the server"""
    return OKSchema()


@router.get(
    '/version',
    summary='Version',
    response_model=VersionSchema,
)
async def version(request: Request):
    """Shows application version"""
    return VersionSchema(version=request.app.version)
