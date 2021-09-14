# How to use Scrapper

With context manager used in normal cases
```python
# manage session with context manager
async with PolygonIOScrapper(apikey) as scrapper:
    resp = await scrapper.scrape('AAPL', '2019-08-10', '2021-09-01', '1m')

```


With FastAPI, we need to manually close aiohttp session
```python
# manage session in FastAPI
...

scrapper = PolygonIOScrapper(apikey)    # make scrapper instance somewhere

...

# define FastAPI shutdown event
@app.on_event("shutdown")
def shutdown_event():
    scrapper.session.close()    # close session when shutdown app
    
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")

```


## API

* 
```python
async def scrape(self, ticker, date_from, date_to, interval):
```
  * __INPUT:__
    * ticker: ticker/symbol of stock in str
    * date_from (want to change this variable to _from__): date to scrape from in a form of %Y-%m-%d in str
    * date_to (want to change this variable to _to_): date to scrape upto in a form of %Y-%m-%d in str
    * interval: usually either '1m', '15m', '1h', or '1d' (m, h, and d are minute, hour, and day each)
  * __OUTPUT:__
    * ticker: list of ticker in str
    * datetime_: list of datetime in str
    * open_: list of open price in float
    * close: list of close price in float
    * high: list of high price in float
    * low: list of low price in float
    * volume: list of volume in int

