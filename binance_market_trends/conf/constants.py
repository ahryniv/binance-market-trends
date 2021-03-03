from enum import Enum

BASE_HTTP_CLIENT_TIMEOUT = 2.0
BINANCE_URL = 'https://api.binance.com'


class PrometheusMetric(str, Enum):
    BINANCE_BTC_TRADES = 'BINANCE_BTC_TRADES'
    BINANCE_GROWING_SYMBOLS_USDT_TOTAL = 'BINANCE_GROWING_SYMBOLS_USDT_TOTAL'
    BINANCE_FALLING_SYMBOLS_USDT_TOTAL = 'BINANCE_FALLING_SYMBOLS_USDT_TOTAL'
    BINANCE_SAME_PRICE_SYMBOLS_USDT_TOTAL = 'BINANCE_SAME_PRICE_SYMBOLS_USDT_TOTAL'
    BINANCE_GROWING_SYMBOLS_USDT_PERCENT = 'BINANCE_GROWING_SYMBOLS_USDT_PERCENT'
