from dataclasses import dataclass
from datetime import timedelta

from binance_market_trends.clients import binance_client
from binance_market_trends.metrics import METRICS, BINANCE_BASE_ASSETS, PrometheusMetric, REDDIT_POSTS_METRIC_TIME, \
    REDDIT_METRICS_KEYWORDS
from binance_market_trends.services import RedditService


@dataclass
class PricesChange:
    growing: int
    falling: int
    growing_percent: int
    same_price: int


class MetricsService:
    """Service managing Prometheus metrics"""

    async def update_metrics(self) -> None:
        """Update metrics"""
        # TODO: run concurrently
        await self.update_binance_metrics()
        await self.update_reddit_metrics()

    async def update_binance_metrics(self) -> None:
        """Update Binance related metrics"""
        for asset in BINANCE_BASE_ASSETS:
            prices_changes = await self.prices_change(base_asset=asset)
            METRICS[PrometheusMetric.BINANCE_GROWING_PAIRS_TOTAL].labels(asset).set(prices_changes.growing)
            METRICS[PrometheusMetric.BINANCE_FALLING_PAIRS_TOTAL].labels(asset).set(prices_changes.falling)
            METRICS[PrometheusMetric.BINANCE_GROWING_PAIRS_PERCENT].labels(asset).set(prices_changes.growing_percent)
            METRICS[PrometheusMetric.BINANCE_SAME_PRICE_PAIRS_TOTAL].labels(asset).set(prices_changes.same_price)

    async def update_reddit_metrics(self) -> None:
        """Update Reddit related metrics
        Idea for optimization: merge all these metrics into one or group them if count of labels will grow
        """
        for keyword in REDDIT_METRICS_KEYWORDS:
            posts_count = await RedditService().get_last_posts_count(
                last=timedelta(minutes=REDDIT_POSTS_METRIC_TIME),
                search_keyword=keyword,
            )
            METRICS[PrometheusMetric.REDDIT_POSTS_TOTAL].labels(keyword).set(posts_count)

    @staticmethod
    async def prices_change(base_asset: str) -> PricesChange:
        """Get prices changes to the asset in Binance"""
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
