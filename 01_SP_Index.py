
#Import libraries
import streamlit as st
import datetime as dt
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

#Set a wide page layout
st.set_page_config(layout = 'wide')

#Index Download
start = dt.datetime(1990, 1, 1)
end = dt.datetime(2022, 12, 1)
sp = yf.download('^GSPC', start, end)

#Tickers from wikipedia list of S&P 500 companies.
sp500_url = "https://en.wikipedia.org//wiki/List_of_S&P_500_companies"
ticker = pd.read_html(sp500_url)
ticker = ticker[0]
ticker_list = list(ticker['Symbol'].values)

#Title
st.title('S&P 500 Index')
st.markdown('***')

#Row A Columns
ac1, ac2 = st.columns(2)

#Bar Chart
with ac1:
    st.markdown('### GICS Sector')

    group = ticker.groupby(by = 'GICS Sector')['Symbol'].count()
    x = group.tolist()
    y = group.index.tolist()
    
    fig = px.pie(values = x, names = y, title = 'Sector')
    st.plotly_chart(fig, use_container_width=True)

#Index Volume
with ac2:
    st.markdown('### Index Volume')
    
    xslider = st.slider('Choose the date range: ', value = (start, end))
    y = sp['Volume'].loc[xslider[0]:xslider[1]]

    fig = px.line(y = y, labels = {'x':'Date', 'y':'Shares Traded'})
    st.plotly_chart(fig, use_container_width=True)

#OHLC
st.markdown('### Index OHLC')
    
x = sp.index.values
y1 = sp['Open'].values
y2 = sp['High'].values
y3 = sp['Low'].values
y4 = sp['Close'].values

fig = go.Figure(data = [go.Candlestick(x = x, open = y1, high = y2, low = y3, close = y4)])
st.plotly_chart(fig, use_container_width = True)

#Row C Columns
ac4, ac5 = st.columns(2)

#Market Capitalization
with ac4:
    st.markdown('### Market Capitalization')

    sp['Total Traded'] = sp['Adj Close'] * sp['Volume']

    xslider2 = st.slider('Date Range: ', value = (start, end))

    y = sp['Total Traded'].loc[xslider2[0]:xslider2[1]]

    fig = px.line(y = y, labels = {'x':'Date', 'y':'Total Money Traded'})
    st.plotly_chart(fig, use_container_width=True)

#Daily Percentage Change
with ac5:
    st.markdown('### Daily Percentage Change')

    x = (sp['Close']/sp['Close'].shift(1)) - 1

    fig = px.histogram(x = x, labels = {'x':'Percentage Return', 'y':'Frequency'})
    st.plotly_chart(fig, use_container_width=True)

