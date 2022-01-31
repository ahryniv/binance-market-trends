from .base_http_client import BaseHTTPClient
from .binance_client import BinanceClient
from .reddit_client import RedditClient
from ..conf import constants

binance_client = BinanceClient(constants.BINANCE_URL)
reddit_client = RedditClient(constants.REDDIT_URL)
