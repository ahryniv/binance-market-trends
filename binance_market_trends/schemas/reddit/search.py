from datetime import datetime
from typing import List

from pydantic import BaseModel


class RedditSearchResultData(BaseModel):
    id: str
    url: str
    subreddit: str
    created_utc: datetime


class RedditSearchResult(BaseModel):
    kind: str
    data: RedditSearchResultData


class RedditSearchResponse(BaseModel):
    after: str
    dist: int
    children: List[RedditSearchResult]
