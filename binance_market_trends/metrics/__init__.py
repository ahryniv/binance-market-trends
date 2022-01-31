from enum import Enum

from prometheus_client import Gauge


class PrometheusMetric(str, Enum):
    BINANCE_GROWING_PAIRS_TOTAL = 'binance_growing_pairs_total'
    BINANCE_FALLING_PAIRS_TOTAL = 'binance_falling_pairs_total'
    BINANCE_SAME_PRICE_PAIRS_TOTAL = 'binance_same_price_pairs_total'
    BINANCE_GROWING_PAIRS_PERCENT = 'binance_growing_pairs_percent'
    REDDIT_POSTS_TOTAL = 'reddit_posts_total'


REDDIT_POSTS_METRIC_TIME = 15
BINANCE_BASE_ASSETS = ['BUSD', 'USDT', 'BTC']
REDDIT_METRICS_KEYWORDS = ['btc', 'cryptocurrency', 'bitcoin', 'crypto', 'doge', 'dogecoin']


BINANCE_GROWING_PAIRS_TOTAL = Gauge(
    PrometheusMetric.BINANCE_GROWING_PAIRS_TOTAL,
    'Growing pairs to [asset] in Binance market total',
    labelnames=('asset',),
)

BINANCE_FALLING_PAIRS_TOTAL = Gauge(
    PrometheusMetric.BINANCE_FALLING_PAIRS_TOTAL,
    'Falling pairs to {{asset}} in Binance market total',
    labelnames=('asset',),
)

BINANCE_GROWING_PAIRS_PERCENT = Gauge(
    PrometheusMetric.BINANCE_GROWING_PAIRS_PERCENT.lower(),
    'Percent of Growing pairs to [asset] in Binance market',
    labelnames=('asset',),
)

BINANCE_SAME_PRICE_PAIRS_TOTAL = Gauge(
    PrometheusMetric.BINANCE_SAME_PRICE_PAIRS_TOTAL.lower(),
    'Pairs with same price to [asset] in Binance market total',
    labelnames=('asset',),
)

REDDIT_POSTS_TOTAL = Gauge(
    PrometheusMetric.REDDIT_POSTS_TOTAL.lower(),
    f'New posts count for last {REDDIT_POSTS_METRIC_TIME}m',
    labelnames=('keyword',),
)


METRICS = {
    PrometheusMetric.BINANCE_GROWING_PAIRS_TOTAL: BINANCE_GROWING_PAIRS_TOTAL,
    PrometheusMetric.BINANCE_FALLING_PAIRS_TOTAL: BINANCE_FALLING_PAIRS_TOTAL,
    PrometheusMetric.BINANCE_GROWING_PAIRS_PERCENT: BINANCE_GROWING_PAIRS_PERCENT,
    PrometheusMetric.BINANCE_SAME_PRICE_PAIRS_TOTAL: BINANCE_SAME_PRICE_PAIRS_TOTAL,
    PrometheusMetric.REDDIT_POSTS_TOTAL: REDDIT_POSTS_TOTAL,
}
