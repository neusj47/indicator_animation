# -*- coding: utf-8 -*-
# TICKER별 수익률, 거래량 animation을 시각화하는 함수
# 날짜를 animation 축으로 설정하여 TICKER별 수익률, 거래량 추이를 시각화합니다.
# TICKER별, 수익률, 거래량을 Input으로 하여 Output인 Graph를 산출합니다.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime
import pandas_datareader.data as web


# 기간을 입력합니다.
start = datetime.datetime(2020, 8, 1)
end = datetime.datetime.now()

# TICKER를 입력합니다.
TICKER = ['AAPL','TSLA','MSFT','AMZN','GOOGL','FB']

# 수익률, 거래량 데이터를 산출합니다.
dfs = web.DataReader(TICKER[0], 'yahoo', start, end)
dfs.reset_index(inplace=True)
dfs.set_index("Date", inplace=True)
dfs['Return'] = (dfs['Close'] / dfs['Close'].shift(1)) - 1
dfs['Return(cum)'] = (1 + dfs['Return']).cumprod()
dfs = dfs.dropna()
dfs.loc[:,'TICKER'] = TICKER[0]
df = dfs

for i in range(1,len(TICKER)):
    start = datetime.datetime(2020, 8, 1)
    end = datetime.datetime.now()
    dfs = web.DataReader(TICKER[i], 'yahoo', start, end)
    dfs.reset_index(inplace=True)
    dfs.set_index("Date", inplace=True)
    dfs['Return'] = (dfs['Close'] / dfs['Close'].shift(1)) - 1
    dfs['Return(cum)'] = (1 + dfs['Return']).cumprod()
    dfs = dfs.dropna()
    dfs.loc[:,'TICKER'] = TICKER[i]
    df = df.append(dfs)

# 데이터타입(Date)변환 문제로 csv 저장 후, 다시 불러옵니다. (파일 경로 설정 필요!!)
df = df.reset_index().rename(columns={"index": "id"})
df.to_csv('pricevolume.csv', index=False, encoding='cp949')
df = pd.read_csv('..../pricevolume.csv')

animations = {
    'Return(cum)': px.scatter(
        df, x="TICKER", y="Return(cum)", animation_frame= "Date",
        animation_group="TICKER", size="Volume",color="TICKER",hover_name="TICKER", size_max=55, range_y=[0,3]),
    'Volume': px.bar(
        df, x="TICKER", y="Volume",color="TICKER",
        animation_frame="Date", range_y=[0,200000000]),
  }

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Return, Volume Animation"),
    dcc.RadioItems(
        id='selection',
        options=[{'label': x, 'value': x} for x in animations],
        value='Return(cum)'
    ),
    dcc.Graph(id="graph"),
])

# 반응형 그래프를 위한 Callback 함수를 정의합니다.
# Input : 날짜, TICKER별 데이터
# Output : Graph
@app.callback(
    Output("graph", "figure"),
    [Input("selection", "value")])
def display_animated_graph(s):
    return animations[s]

app.run_server(debug=True)

