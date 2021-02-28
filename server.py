import uvicorn

from binance_market_trends.app import create_app
from binance_market_trends.conf.logging import LOG_CONFIG
from binance_market_trends.conf.settings import settings

app = create_app()


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=settings.API_PORT,
        log_level=settings.LOG_LEVEL.value.lower(),
        log_config=LOG_CONFIG,
    )
