# Fin Crawler


## Features
- Fetch Finalcial data like stock price or future price etc.

## Current Support List
- Taiwan stock price (每日各股股價) - tw_stock_price_daily
- Taiwan stock price (每月單一股票股價) - tw_stock_price
- Taiwan 3 insititutional investors daily records (每日三大法人買賣超) - tw_institutional_investors_daily
- Taiwan IPO company info (公司資訊) - tw_stock_info
## Example

### Supported List
```
>>> from fin_crawler import FinCrawler
>>> FinCrawler.crawler_list
['tw_stock_price_daily',
 'tw_stock_price',
 'tw_institutional_investors_daily',
 'tw_stock_info']
```

### Get Crawler Params Example
For each crawler you should pass in params and this will get you example of params
```
>>> params_example = FinCrawler.params_example('tw_stock_price_daily')
爬取其中一天全部股票的價格
ex:{'date': '20220920'}
>>> params_example
{'date': '20220920'}
```

### Get Data Example
```
# get stock data
>>> stock_price = FinCrawler.get('tw_stock_price_daily',{'date':'20220920'})
# check stock data keys
>>> stock_price[0]
{'stock_id': '0050',
 'stock_name': '元大台灣50',
 'volume': 5999746.0,
 'trade_num': 7093.0,
 'trade_amount': 675492164.0,
 'open': 112.55,
 'high': 113.15,
 'low': 112.25,
 'close': 113.05,
 'last_buy_price': 113.0,
 'last_buy_volume': 205.0,
 'last_sell_price': 113.05,
 'last_sell_volume': 9.0,
 'PE': 0.0,
 'spread': 1.0,
 'date': '20220920'}
```