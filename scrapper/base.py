import asyncio
import aiohttp

from abc import ABC, abstractmethod
from functools import reduce
from urllib.parse import urljoin


class Scrapper(ABC):
    def __init__(self, apikey):
        self.apikey = apikey
        self.session = aiohttp.ClientSession()
        self.url = ''
        
    @abstractmethod
    async def scrape(self, ticker, date_from, date_to, interval):
        """Method to scrape stock data and must be implemented as the following:
        1. create endpoint
        2. create query
        3. call self._request to build response
        """
        pass
    
    async def _request(self, endpoint, query):
        async with self.session.get(endpoint, params=query) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                resp.raise_for_status()
                
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        # With FastAPI, session needs to be closed when sever closes
        # https://fastapi.tiangolo.com/advanced/events/
        await self.session.close()
        