#Import libraries
import streamlit as st
import datetime as dt
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Download Data
start = dt.datetime(1990, 1, 1)
end = dt.datetime(2022, 12, 1)

amzn = yf.download('AMZN', start, end)
nke = yf.download('NKE', start, end)
mcd = yf.download('MCD', start, end)

nke_dividend = pd.read_csv("/Users/snovanna/Documents/Cursos/Henry Data Science/Proyectos/PI02/Nike, Inc. Common Stock (NKE) Dividend History _ Nasdaq.csv")
mcd_dividend = pd.read_csv("/Users/snovanna/Documents/Cursos/Henry Data Science/Proyectos/PI02/McDonald's Corporation Common Stock (MCD) Dividend History _ Nasdaq.csv")

#Title
st.title('Key Performance Indicators (KPIs)')

#Tabs
tab1, tab2, tab3 = st.tabs(['Yearly Stock % Price Change', 'Dividend Yield %', 'Transacted Money Change'])

with tab1:
    #Yearly Stock % Price Change
    amzn['Returns'] = (amzn['Adj Close']/amzn['Adj Close'].shift(1))-1
    nke['Returns'] = (nke['Adj Close']/nke['Adj Close'].shift(1))-1
    mcd['Returns'] = (mcd['Adj Close']/mcd['Adj Close'].shift(1))-1

    amzn_yspc = amzn.groupby(amzn.index.year)['Returns'].mean()
    nke_yspc = nke.groupby(nke.index.year)['Returns'].mean()
    mcd_yspc = mcd.groupby(mcd.index.year)['Returns'].mean()

    x1 = amzn_yspc.index.values
    x2 = nke_yspc.index.values
    x3 = mcd_yspc.index.values

    y1 = amzn_yspc.values
    y2 = nke_yspc.values
    y3 = mcd_yspc.values

    fig = make_subplots(
            rows = 3, 
            cols = 1,
            subplot_titles = ("Amazon", "Nike", "McDonalds")
            )

    fig.append_trace(go.Scatter(
            x = x1,
            y = y1
        ), row = 1, col = 1)

    fig.append_trace(go.Scatter(
            x = x2,
            y = y2
        ), row = 2, col = 1)

    fig.append_trace(go.Scatter(
            x = x3,
            y = y3
        ), row = 3, col = 1)

    fig.update_yaxes(
            title_text = 'Price Change (%)',
            row = 1,
            col = 1
        )

    fig.update_yaxes(
            title_text = 'Price Change (%)',
            row = 2,
            col = 1
        )

    fig.update_yaxes(
            title_text = 'Price Change (%)',
            row = 3,
            col = 1
        )

    fig.update_xaxes(
            title_text = 'Date',
            row = 3,
            col = 1
        )

    fig.update_layout(title_text = 'Yearly Percent Returns')
    st.plotly_chart(fig, use_container_width = True)

with tab2:
    #Dividend Yield %
    nke_asp = nke.groupby(nke.index.year)['Adj Close'].mean()
    mcd_asp = mcd.groupby(mcd.index.year)['Adj Close'].mean()

    #Nike
    nke_dividend['PAYMENT DATE'] = pd.to_datetime(nke_dividend['PAYMENT DATE'])
    nke_dividend = nke_dividend[['PAYMENT DATE', 'CASH AMOUNT']]
    nke_dividend['CASH AMOUNT'] = nke_dividend['CASH AMOUNT'].str.strip('$')
    nke_dividend['CASH AMOUNT'] = pd.to_numeric(nke_dividend['CASH AMOUNT'])
    nke_dividend = nke_dividend.groupby(nke_dividend['PAYMENT DATE'].dt.year)['CASH AMOUNT'].sum()
    nke_asp = pd.DataFrame({'year': nke_asp.index, 'avg share price': nke_asp.values})
    nke_dividend = pd.DataFrame({'year': nke_dividend.index, 'dividend': nke_dividend.values})
    nke_dyp = nke_asp.set_index('year').join(nke_dividend.set_index('year'))

    #McDonalds
    mcd_dividend['PAYMENT DATE'] = pd.to_datetime(mcd_dividend['PAYMENT DATE'])
    mcd_dividend = mcd_dividend[['PAYMENT DATE', 'CASH AMOUNT']]
    mcd_dividend = mcd_dividend[mcd_dividend['PAYMENT DATE'].dt.year > 1990]
    mcd_dividend['CASH AMOUNT'] = mcd_dividend['CASH AMOUNT'].str.strip('$')
    mcd_dividend['CASH AMOUNT'] = pd.to_numeric(mcd_dividend['CASH AMOUNT'])
    mcd_dividend = mcd_dividend.groupby(mcd_dividend['PAYMENT DATE'].dt.year)['CASH AMOUNT'].sum()
    mcd_asp = pd.DataFrame({'year': mcd_asp.index, 'avg share price': mcd_asp.values})
    mcd_dividend = pd.DataFrame({'year': mcd_dividend.index, 'dividend': mcd_dividend.values})
    mcd_dyp = mcd_asp.set_index('year').join(mcd_dividend.set_index('year'))

    nke_dyp['dividend yield'] = (nke_dyp['dividend'] / nke_dyp['avg share price'])*100
    mcd_dyp['dividend yield'] = (mcd_dyp['dividend'] / mcd_dyp['avg share price'])*100

    x1 = nke_dyp.index.values
    x2 = mcd_dyp.index.values

    y1 = nke_dyp['dividend yield'].values
    y2 = mcd_dyp['dividend yield'].values

    fig = make_subplots(
        rows = 2, 
        cols = 1,
        subplot_titles = ("Nike", "McDonalds")
        )

    fig.append_trace(go.Scatter(
        x = x1,
        y = y1
        ), row = 1, col = 1)
    
    fig.append_trace(go.Scatter(
        x = x2,
        y = y2
        ), row = 2, col = 1)
    
    fig.update_yaxes(
        title_text = 'Dividend Yield %',
        row = 1,
        col = 1)
    
    fig.update_yaxes(
        title_text = 'Dividend Yield %',
        row = 2,
        col = 1)
    
    fig.update_xaxes(
        title_text = 'Date',
        row = 2,
        col = 1)

    fig.update_layout(title_text = 'Dividend Yield %')
    st.plotly_chart(fig, use_container_width = True)
    
with tab3:
    #Transacted Money Change
    amzn['Total Traded'] = amzn['Adj Close'] * amzn['Volume']
    nke['Total Traded'] = nke['Adj Close'] * nke['Volume']
    mcd['Total Traded'] = mcd['Adj Close'] * mcd['Volume']

    amzn_tmc = pd.DataFrame(amzn.groupby(amzn.index.year)['Total Traded'].mean())
    amzn_tmc['Transacted Money Change'] = (amzn_tmc['Total Traded']/amzn_tmc['Total Traded'].shift(1))-1

    nke_tmc = pd.DataFrame(nke.groupby(nke.index.year)['Total Traded'].mean())
    nke_tmc['Transacted Money Change'] = (nke_tmc['Total Traded']/nke_tmc['Total Traded'].shift(1))-1

    mcd_tmc = pd.DataFrame(mcd.groupby(mcd.index.year)['Total Traded'].mean())
    mcd_tmc['Transacted Money Change'] = (mcd_tmc['Total Traded']/mcd_tmc['Total Traded'].shift(1))-1

    x1 = amzn_tmc.index.values
    x2 = nke_tmc.index.values
    x3 = mcd_tmc.index.values

    y1 = amzn_tmc['Transacted Money Change'].values
    y2 = nke_tmc['Transacted Money Change'].values
    y3 = mcd_tmc['Transacted Money Change'].values

    fig = make_subplots(
            rows = 3, 
            cols = 1,
            subplot_titles = ("Amazon", "Nike", "McDonalds")
            )

    fig.append_trace(go.Scatter(
            x = x1,
            y = y1
        ), row = 1, col = 1)

    fig.append_trace(go.Scatter(
            x = x2,
            y = y2
        ), row = 2, col = 1)

    fig.append_trace(go.Scatter(
            x = x3,
            y = y3
        ), row = 3, col = 1)

    fig.update_yaxes(
            title_text = 'Money Transacted (%)',
            row = 2,
            col = 1
        )

    fig.update_xaxes(
            title_text = 'Date',
            row = 3,
            col = 1
        )

    fig.update_layout(title_text = 'Transacted Money Change')
    st.plotly_chart(fig, use_container_width = True)

c1, c2, c3 = st.columns(3)

#Get last 3 years
amzn_3y = amzn.loc['2019-01-01' : '2022-12-31']
nke_3y = nke.loc['2019-01-01' : '2022-12-31']
mcd_3y = mcd.loc['2019-01-01' : '2022-12-31']

#Adj Close Price by Weekday
amzn_day = amzn_3y.resample('D').mean()
amzn_weekday = amzn_day.groupby(amzn_day.index.dayofweek).mean()

nke_day = nke_3y.resample('D').mean()
nke_weekday = nke_day.groupby(nke_day.index.dayofweek).mean()

mcd_day = mcd_3y.resample('D').mean()
mcd_weekday = mcd_day.groupby(mcd_day.index.dayofweek).mean()

with c1:
    #Amazon Day of the Week
    st.subheader('Amazon')
    amzn_weekday.index = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    x = amzn_weekday.index.values
    y = amzn_weekday['Adj Close']

    fig = px.line(x = x, y = y, labels = {'x':'Day of the Week', 'y':'Mean Stock Price'})
    st.plotly_chart(fig, use_container_width=True)

with c2:
    #Nike Day of the Week
    st.subheader('Nike')
    nke_weekday.index = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    x = nke_weekday.index.values
    y = nke_weekday['Adj Close']

    fig = px.line(x = x, y = y, labels = {'x':'Day of the Week', 'y':'Mean Stock Price'})
    st.plotly_chart(fig, use_container_width=True)

with c3:
    #McDonalds Day of the Week
    st.subheader('McDonalds')
    mcd_weekday.index = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    x = mcd_weekday.index.values
    y = mcd_weekday['Adj Close'].values

    fig = px.line(x = x, y = y, labels = {'x':'Day of the Week', 'y':'Mean Stock Price'})
    st.plotly_chart(fig, use_container_width=True)