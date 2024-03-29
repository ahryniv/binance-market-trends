import json
from typing import Optional


class HTTPClientException(Exception):
    def __init__(self, url: str, status_code: Optional[int], response_text: str):
        self.url = url
        self.status_code = status_code
        self.response_text = response_text

    def json(self):
        try:
            return json.loads(self.response_text)

        except json.decoder.JSONDecodeError:
            return

    def __str__(self) -> str:
        return f'URL {self.url} responded with {self.status_code}. RESPONSE: {self.response_text}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} status_code={self.status_code}>'


class BinanceClientException(HTTPClientException):
    pass


class RedditClientException(HTTPClientException):
    pass
