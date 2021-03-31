from datetime import timedelta, datetime, timezone

from binance_market_trends.database import db
from binance_market_trends.database.models import RedditPost


class RedditService:
    @staticmethod
    async def get_last_posts_count(last: timedelta, search_keyword: str = None) -> int:
        now_utc = datetime.now(tz=timezone.utc).replace(tzinfo=None)
        query = db.select([db.func.count()]).where(
            RedditPost.reddit_created_utc > now_utc - last
        )
        if search_keyword:
            query = query.where(RedditPost.search_keyword == search_keyword)

        return await query.gino.scalar()
