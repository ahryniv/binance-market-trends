import logging
from datetime import datetime, timedelta, timezone
from time import time
from typing import Dict, Any

from binance_market_trends.clients import reddit_client
from binance_market_trends.database.models import RedditPost
from binance_market_trends.schemas.reddit import RedditSearchResponse
from binance_market_trends.scrapers import BaseScraper

logger = logging.getLogger(__name__)


class RedditScraper(BaseScraper):
    def __init__(self, *args, search_keyword: str, depth: timedelta, **kwargs):
        super(RedditScraper, self).__init__(*args, **kwargs)
        self.search_keyword = search_keyword
        self.depth = depth  # If DB is empty it will be used to determine the time depth of scraping
        self._stored_data_count = 0

    async def scrape(self):
        self._stored_data_count = 0
        try:
            last_post_date = await self._get_last_post_date()
            after = None
            while True:
                response: RedditSearchResponse = await reddit_client.search(q=self.search_keyword, after=after)
                data = self._generate_data_from_response(response, last_post_date)
                await self._filter_data(data)
                await self._store_data(data)
                if not data or len(data) < response.dist:
                    break

                after = response.after

        except Exception as err:
            logger.exception(err)

    async def _get_last_post_date(self) -> datetime:  # TODO: move to service
        """Get date of the last post searched by this keyword"""
        query = RedditPost.query.where(
            RedditPost.search_keyword == self.search_keyword
        ).order_by(
            RedditPost.reddit_created_utc.desc()
        )
        post = await query.gino.first()
        if not post:
            return datetime.now(tz=timezone.utc).replace(tzinfo=None) - self.depth
        return post.reddit_created_utc

    def _generate_data_from_response(
            self, response: RedditSearchResponse, last_post_date: datetime) -> Dict[str, Dict[str, Any]]:
        """Generate data from Reddit response"""
        return {post.data.id: dict(
            reddit_kind=post.kind,
            reddit_id=post.data.id,
            reddit_url=post.data.url,
            subreddit=post.data.subreddit,
            reddit_created_utc=post.data.created_utc.replace(tzinfo=None),
            search_keyword=self.search_keyword,
        ) for post in response.children if post.data.created_utc.replace(tzinfo=None) >= last_post_date}

    @staticmethod
    async def _filter_data(data: Dict[str, Dict[str, Any]]):
        """Filter already existing posts from data"""
        existing_posts = await RedditPost.query.where(
            RedditPost.reddit_id.in_(data.keys())
        ).gino.all()
        for post in existing_posts:
            del data[post.reddit_id]
        if existing_posts:
            logger.debug(f'filtered {len(existing_posts)} posts of {len(data)} total')

    async def _store_data(self, data: Dict[str, Dict[str, Any]]):  # TODO: move to service
        """Store Reddit posts to the DB"""
        if data:
            await RedditPost.insert().gino.all(list(data.values()))
            self._stored_data_count += len(data)

    def _end_log(self):
        logger.info(f'Finished scraping with {self.__class__}. Time: {time() - self._last_start_time}s. '
                    f'Created {self._stored_data_count} records')
