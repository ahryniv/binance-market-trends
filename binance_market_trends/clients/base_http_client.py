import logging
from typing import Type
from urllib.parse import urljoin

import httpx

from binance_market_trends.conf import constants
from binance_market_trends.exceptions import HTTPClientException

logger = logging.getLogger(__name__)


class BaseHTTPClient:
    """Base HTTP client"""

    EXC_CLASS: Type[HTTPClientException]
    TIMEOUT: float = constants.BASE_HTTP_CLIENT_TIMEOUT

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, url: str, **kwargs) -> httpx.Response:
        return self._request('GET', url, **kwargs)

    async def aget(self, url: str, **kwargs) -> httpx.Response:
        return await self._arequest('GET', url, **kwargs)

    def post(self, url: str, **kwargs) -> httpx.Response:
        return self._request('POST', url, **kwargs)

    async def apost(self, url: str, **kwargs) -> httpx.Response:
        return await self._arequest('POST', url, **kwargs)

    def get_url(self, url: str) -> str:
        return urljoin(self.base_url, url)

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make a sync HTTP request"""
        url = self.get_url(url)
        logger.info({'message': f'External request to {url}'})

        try:
            response = httpx.request(method, url, timeout=self.TIMEOUT, **kwargs)
        except httpx.HTTPError as err:
            logger.exception({'message': str(err)})
            raise self.EXC_CLASS(status_code=None, response_text=str(err), url=url)

        logger.info({'message': f'Received response from {url} with status code {response.status_code}'})

        self._check_response(response)
        return response

    async def _arequest(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make an async HTTP request"""
        url = self.get_url(url)
        logger.info({'message': f'External request to {url}'})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, timeout=self.TIMEOUT, **kwargs)

        except httpx.HTTPError as err:
            logger.exception({'message': str(err)})
            raise self.EXC_CLASS(status_code=None, response_text=str(err), url=url)

        logger.info({'message': f'Received response from {url} with status code {response.status_code}'})

        self._check_response(response)
        return response

    def _check_response(self, response: httpx.Response) -> None:
        if response.is_error:
            raise self.EXC_CLASS(
                status_code=response.status_code,
                response_text=response.text,
                url=str(response.url),
            )
