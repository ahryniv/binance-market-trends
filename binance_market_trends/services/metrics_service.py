from dataclasses import dataclass

from binance_market_trends.clients import binance_client


@dataclass
class PricesChange:
    growing: int
    falling: int
    growing_percent: int
    same_price: int


class MetricsService:
    @staticmethod
    async def prices_change(base_asset: str = 'USDT') -> PricesChange:
        prices = await binance_client.ticker_24_hr()
        price_changes = [price.price_change for price in prices if price.symbol.endswith(base_asset)]
        growing = sum(price_change > 0 for price_change in price_changes)
        falling = sum(price_change < 0 for price_change in price_changes)
        same_price = sum(price_change == 0 for price_change in price_changes)
        return PricesChange(
            growing=growing,
            falling=falling,
            growing_percent=growing / (growing + falling) * 100,
            same_price=same_price,
        )
