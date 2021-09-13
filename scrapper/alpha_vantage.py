import asyncio
import aiohttp

from functools import reduce
from urllib.parse import urljoin


# TODO: Make general scrapper and its subclass
class Scrapper:
    def __init__(self, apikey):
        self.apikey = apikey
        self.session = aiohttp.ClientSession()
        self.url = 'https://www.alphavantage.co/'    # alpha vantage
        
    async def get(self, ticker, date_from, date_to, interval):
        # https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
        endpoint = reduce(urljoin, [self.url, 'query'])
        query = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': ticker,
            'apikey': self.apikey
        }
        resp = await self._request(endpoint, query)
        return resp
    
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
        
if __name__ == '__main__':
    async def main():
        async with Scrapper('demo') as scrapper:
            res = await scrapper.get('AAPL', '', '', '')
            print(res)
            
    asyncio.run(main())