import asyncio
import aiohttp

from functools import reduce
from urllib.parse import urljoin
from base import Scrapper


class PolygonIOScrapper(Scrapper):
    def __init__(self, apikey):
        self.apikey = apikey
        self.session = aiohttp.ClientSession()
        self.url = 'https://api.polygon.io/'    # polygon io
        self.unit_map = {
            'm': 'minute',
            'h': 'hour',
            'd': 'day',
        }
        
    async def scrape(self, ticker, date_from, date_to, interval):
        multiplier = interval[: -1]
        timespan = self.unit_map[interval[-1]]
        # https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2020-10-14/2020-10-14?adjusted=true&sort=asc&limit=120&apiKey=demo
        endpoint = reduce(urljoin, [self.url, 'v2/', 'aggs/', 'ticker/'f'{ticker}/', 'range/', 
                                    f'{multiplier}/', f'{timespan}/', f'{date_from}/', f'{date_to}/'])
        query = {
            'adjsuted': 'true',
            'sort': 'asc',
            'limit': '120',
            'apikey': self.apikey,
        }
        resp = await self._request(endpoint, query)
        data = zip(*[[resp['ticker'], resp['results'][i]['t'], resp['results'][i]['o'], 
                      resp['results'][i]['c'], resp['results'][i]['h'], 
                      resp['results'][i]['l'], resp['results'][i]['v'], None] for i in range(resp['queryCount'])])
        ticker, timestamp, open_, close, high, low, volumn, split_coefficient = data
        datetime_ = list(map(lambda x: datetime.fromtimestamp(int(x / 1000)).__str__(), timestamp))
        return ticker, datetime_, open_, close, high, low, volumn, split_coefficient