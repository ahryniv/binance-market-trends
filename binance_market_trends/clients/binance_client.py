import logging
from datetime import timedelta, datetime, timezone
from typing import List

import funcy

from binance_market_trends.clients import BaseHTTPClient
from binance_market_trends.schemas.binance import Symbol24PriceSchema

logger = logging.getLogger(__name__)


class BinanceClient(BaseHTTPClient):
    """HTTP Client for the Binance"""

    def __init__(self, *args, **kwargs):
        super(BinanceClient, self).__init__(*args, **kwargs)
        self.ticker_24_hr_cached_data = None
        self.ticker_24_hr_last_request = None
        self.ticker_24_hr_timeout = timedelta(minutes=1)

    async def ticker_24_hr(self) -> List[Symbol24PriceSchema]:
        """24 hour rolling window price change statistics
        Weight: 1 for a single symbol;
                40 when the symbol parameter is omitted;
        """
        now = datetime.now(tz=timezone.utc)
        if not self.ticker_24_hr_cached_data or now - self.ticker_24_hr_timeout > self.ticker_24_hr_last_request:
            response = await self.aget('/api/v3/ticker/24hr')
            self.ticker_24_hr_cached_data = [Symbol24PriceSchema(**symbol) for symbol in response.json()]
            self.ticker_24_hr_last_request = now
        else:
            logger.info('Ticker 24: use cache')
        return self.ticker_24_hr_cached_data
