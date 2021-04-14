import asyncio
import logging.config
from datetime import timedelta

from binance_market_trends.conf.logging import LOG_CONFIG
from binance_market_trends.database.db import connect_db, disconnect_db
from binance_market_trends.metrics import REDDIT_METRICS_KEYWORDS
from binance_market_trends.scrapers import RedditScraper

SCRAPERS = [
    RedditScraper(timeout=timedelta(minutes=1), search_keyword=keyword, depth=timedelta(minutes=105))
    for keyword in REDDIT_METRICS_KEYWORDS
]


if __name__ == '__main__':
    logging.config.dictConfig(LOG_CONFIG)
    loop = asyncio.get_event_loop()

    loop.run_until_complete(connect_db())

    for scraper in SCRAPERS:
        loop.create_task(scraper.run_with_timeout())

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(disconnect_db())
        loop.close()
