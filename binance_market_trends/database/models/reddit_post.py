from binance_market_trends.database import db


class RedditPost(db.Model):
    __tablename__ = 'reddit_posts'

    id = db.Column(db.Integer(), primary_key=True)
    reddit_kind = db.Column(db.String(2), nullable=False)
    reddit_id = db.Column(db.String(20), unique=True, nullable=False)
    reddit_url = db.Column(db.String(), nullable=False)
    subreddit = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
