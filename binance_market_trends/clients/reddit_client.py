import httpx

from binance_market_trends import __version__
from binance_market_trends.clients import BaseHTTPClient
from binance_market_trends.exceptions import RedditClientException
from binance_market_trends.schemas.reddit import RedditSearchResponse


class RedditClient(BaseHTTPClient):
    """HTTP Client for the Reddit

    Docs: https://www.reddit.com/dev/api/

    Note: Clients connecting via OAuth2 may make up to 60 requests per minute.
        Response headers to monitor limits:
        X-Ratelimit-Used: Approximate number of requests used in this period
        X-Ratelimit-Remaining: Approximate number of requests left to use
        X-Ratelimit-Reset: Approximate number of seconds to end of period
    """

    EXC_CLASS = RedditClientException
    USER_AGENT = f'python:PlayGround:v{__version__} (by u/Obvious-List8224)'

    class ROUTES:
        ACCESS_TOKEN = '/api/v1/access_token'
        SEARCH = '/search.json'

    # async def get_access_token(self):  # TODO: Cache token
    #     """Retrieve access token"""
    #     self.client_auth = HTTPBasicAuth(settings.REDDIT_CLIENT_ID, settings.REDDIT_CLIENT_SECRET)
    #     response = await self.apost(
    #         self.ROUTES.ACCESS_TOKEN,
    #         auth=self.client_auth,
    #         data={'grant_type': 'client_credentials'}
    #     )
    #     return response.json()['access_token']

    async def search(self, q: str, sort: str = 'new', after: str = None) -> RedditSearchResponse:
        """Search links page.
        https://www.reddit.com/dev/api#GET_search
        """
        params = {'q': q, 'sort': sort}
        if after:
            params['after'] = after
        response = await self.aget(self.ROUTES.SEARCH, params=params)
        return RedditSearchResponse(**response.json()['data'])

    async def _arequest(self, method: str, url: str, **kwargs) -> httpx.Response:
        headers = kwargs.get('headers', {})
        headers['User-Agent'] = self.USER_AGENT
        kwargs['headers'] = headers
        return await super(RedditClient, self)._arequest(method, url, **kwargs)
