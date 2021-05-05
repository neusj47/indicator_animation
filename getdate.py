# TICKER별 가격, 거래량 가져오는 함수입니다.
# 수익률, 누적 수익률 산출합니다.

import datetime
import pandas_datareader.data as web
import pandas as pd
import plotly.express as px

TICKER = ['AAPL','TSLA','MSFT','GOOGL','FB','BABA']

start = datetime.datetime(2020, 11, 1)
end = datetime.datetime.now()
dfs = web.DataReader(TICKER[0], 'yahoo', start, end)
dfs.reset_index(inplace=True)
dfs.set_index("Date", inplace=True)
dfs['Return'] = (dfs['Close'] / dfs['Close'].shift(1)) - 1
dfs['Return(cum)'] = (1 + dfs['Return']).cumprod()
dfs = dfs.dropna()
dfs.loc[:,'TICKER'] = TICKER[0]
df = dfs

for i in range(1,len(TICKER)):
    start = datetime.datetime(2020, 11, 1)
    end = datetime.datetime.now()
    dfs = web.DataReader(TICKER[i], 'yahoo', start, end)
    dfs.reset_index(inplace=True)
    dfs.set_index("Date", inplace=True)
    dfs['Return'] = (dfs['Close'] / dfs['Close'].shift(1)) - 1
    dfs['Return(cum)'] = (1 + dfs['Return']).cumprod()
    dfs = dfs.dropna()
    dfs.loc[:,'TICKER'] = TICKER[i]
    df = df.append(dfs)

print(df)

