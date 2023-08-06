# stock-market-lib

stock-market-lib is a Python library that contains functionality related to stocks and the stock market in general.
It also contains functionality to analyze stock time series.
All classes are considered immutable.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install stock-market-lib.

```bash
pip install stock-market-lib @ git+https://bitbucket.org/MattiasDC/stock-market-lib.git
```

## Usage

```python
import datetime as dt
import pandas as pd
from stock_market.core import StockMarket, Ticker, TickerOHLC, OHLC
from stock_market.ext.indicator import ExponentialMovingAverage

# Creates a ticker QQQ
qqq = Ticker("QQQ")

# Create a stock market that has as start date 1/1/2020, with a single ticker QQQ
sm = StockMarket(dt.date(2020, 1, 1), [qqq])

# Create a new ticker and new stock market that also contains the SPY ticker
spy = Ticker('SPY')
new_sm = sm.add_ticker(spy)

# Create and update OHLC data for ticker SPY
dates = pd.Series([dt.date(2020, 1, 7), dt.date(2020, 1, 8), dt.date(2020, 1, 9)])
open = pd.Series([1, 2, 3])
high = pd.Series([2, 3, 4])
low = pd.Series([0, 1, 2])
close = pd.Series([1.5, 1.2, 2.9])
ohlc = OHLC(dates, open, high, low, close)
new_sm = new_sm.update_ticker(TickerOHLC(spy, ohlc))

# Query OHLC data for ticker SPY
ohlc = new_sm.ohlc(spy)

# Create an EMA2 for the closing values of the SPY ticker
spy_ema2 = ExponentialMovingAverage(2)(ohlc.close)
print(spy_ema2.values)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)