import abc
import asyncio
import logging
from datetime import timedelta
from time import time

logger = logging.getLogger(__name__)


class BaseScraper(metaclass=abc.ABCMeta):
    def __init__(self, timeout: timedelta):
        self.timeout = timeout.seconds
        self._last_start_time = None

    async def run_with_timeout(self) -> None:
        """Run scraper with timeout"""
        while True:
            self._last_start_time = time()
            self._start_log()
            await self.scrape()
            self._end_log()
            await asyncio.sleep(self.timeout)

    def _start_log(self):
        logger.info(f'Started scraping with {self.__class__}')

    def _end_log(self):
        logger.info(f'Finished scraping with {self.__class__}. Time: {time() - self._last_start_time}s')

    @abc.abstractmethod
    async def scrape(self):
        """Do the needed scraping work with set timeout"""
        raise NotImplemented
