import asyncio
import aiohttp

from functools import reduce
from urllib.parse import urljoin
from base import Scrapper


class AlphaVantageScrapper(Scrapper):
    def __init__(self, apikey):
        self.apikey = apikey
        self.session = aiohttp.ClientSession()
        self.url = 'https://www.alphavantage.co/'    # alpha vantage
        
    async def scrape(self, ticker, date_from, date_to, interval):
        # https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
        endpoint = reduce(urljoin, [self.url, 'query'])
        query = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': ticker,
            'apikey': self.apikey
        }
        resp = await self._request(endpoint, query)
        return resp
                
        
if __name__ == '__main__':
    async def main():
        async with AlphaVantageScrapper('demo') as scrapper:
            res = await scrapper.scrape('AAPL', '', '', '')
            print(res)
            
    asyncio.run(main())