#Import libraries
import streamlit as st
import datetime as dt
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Set a wide page layout
st.set_page_config(layout = 'wide')

#Download Data
start = dt.datetime(1990, 1, 1)
end = dt.datetime(2022, 12, 1)

#Getting the tickers from the wikipedia list of S&P 500 companies.
sp500_url = "https://en.wikipedia.org//wiki/List_of_S&P_500_companies"
ticker = pd.read_html(sp500_url)
ticker = ticker[0]
ticker_list = list(ticker['Symbol'].values)

amzn = yf.download('AMZN', start, end)
ebay = yf.download('EBAY', start, end)
bkng = yf.download('BKNG', start, end)
nke = yf.download('NKE', start, end)
vfc = yf.download('VFC', start, end)
rl = yf.download('RL', start, end)
dpz = yf.download('DPZ', start, end)
mcd = yf.download('MCD', start, end)
sbux = yf.download('SBUX', start, end)

#Title
st.title('S&P 500 Companies')
st.markdown('***')

#Bar Chart
st.markdown('### Consumer Discretionary Sector')

group = ticker.query('`GICS Sector` == "Consumer Discretionary"').groupby(by = 'GICS Sub-Industry')['Symbol'].count()
x = group.tolist()
y = group.index.tolist()

fig = px.pie(values = x, names = y, title = 'Sub-industries')
st.plotly_chart(fig, use_container_width=True)

#Tabs
tab1, tab2, tab3 = st.tabs(['Internet & Direct Marketing Retail', 'Apparel, Accesories & Luxury Goods', 'Restaurants'])

#Internet & Direct Marketing Retail
with tab1:
    tc1, tc2 = st.columns(2)
    
    with tc1:
        #Moving Average
        amzn['Mov Av 80'] = amzn['Adj Close'].rolling(80).mean()
        ebay['Mov Av 80'] = ebay['Adj Close'].rolling(80).mean()
        bkng['Mov Av 80'] = bkng['Adj Close'].rolling(80).mean()

        x1 = amzn.index.values
        x2 = ebay.index.values
        x3 = bkng.index.values

        y1 = amzn['Mov Av 80'].values
        y2 = ebay['Mov Av 80'].values
        y3 = bkng['Mov Av 80'].values

        fig = make_subplots(
            rows = 3, 
            cols = 1,
            subplot_titles = ("Amazon", "Ebay", "Booking Holdings Inc")
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
            title_text = 'Stock Price',
            row = 1,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Stock Price',
            row = 2,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Stock Price',
            row = 3,
            col = 1
        )

        fig.update_xaxes(
            title_text = 'Date',
            row = 3,
            col = 1
        )

        fig.update_layout(title_text = 'Moving Average')
        st.plotly_chart(fig, use_container_width = True)

    with tc2:
        #Market Capitalization
        amzn['Total Traded'] = amzn['Adj Close'] * amzn['Volume']
        ebay['Total Traded'] = ebay['Adj Close'] * ebay['Volume']
        bkng['Total Traded'] = bkng['Adj Close'] * bkng['Volume']

        x1 = amzn.index.values
        x2 = ebay.index.values
        x3 = bkng.index.values

        y1 = amzn['Total Traded'].values
        y2 = ebay['Total Traded'].values
        y3 = bkng['Total Traded'].values

        fig = make_subplots(
            rows = 3, 
            cols = 1,
            subplot_titles = ("Amazon", "Ebay", "Booking Holdings Inc")
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
            title_text = 'Total Money Traded',
            row = 1,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Total Money Traded',
            row = 2,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Total Money Traded',
            row = 3,
            col = 1
        )

        fig.update_xaxes(
            title_text = 'Date',
            row = 3,
            col = 1
        )

        fig.update_layout(title_text = 'Market Capitalization Approximate')
        st.plotly_chart(fig, use_container_width = True)
    
    #OHLC
    st.subheader('Click the companys button to see its OHLC graph')
    amzn_button = st.button("Amazon")
    ebay_button = st.button("Ebay")
    bkng_button = st.button("Booking Holdings Inc")

    if amzn_button:

        x = amzn.index.values
        y1 = amzn['Open'].values
        y2 = amzn['High'].values
        y3 = amzn['Low'].values
        y4 = amzn['Close'].values

        fig = go.Figure(data=go.Ohlc(x = x, open = y1, high = y2, low = y3, close = y4))
        st.plotly_chart(fig, use_container_width = True)
    
    if ebay_button:

        x = ebay.index.values
        y1 = ebay['Open'].values
        y2 = ebay['High'].values
        y3 = ebay['Low'].values
        y4 = ebay['Close'].values

        fig = go.Figure(data=go.Ohlc(x = x, open = y1, high = y2, low = y3, close = y4))
        st.plotly_chart(fig, use_container_width = True)

    if bkng_button:

        x = bkng.index.values
        y1 = bkng['Open'].values
        y2 = bkng['High'].values
        y3 = bkng['Low'].values
        y4 = bkng['Close'].values

        fig = go.Figure(data=go.Ohlc(x = x, open = y1, high = y2, low = y3, close = y4))
        st.plotly_chart(fig, use_container_width = True)

#Apparel, Accessories & Luxury Goods
with tab2:
    tc1, tc2 = st.columns(2)

    with tc1:
        #Moving Average
        nke['Mov Av 80'] = nke['Adj Close'].rolling(80).mean()
        vfc['Mov Av 80'] = vfc['Adj Close'].rolling(80).mean()
        rl['Mov Av 80'] = rl['Adj Close'].rolling(80).mean()

        x1 = nke.index.values
        x2 = vfc.index.values
        x3 = rl.index.values

        y1 = nke['Mov Av 80'].values
        y2 = vfc['Mov Av 80'].values
        y3 = rl['Mov Av 80'].values

        fig = make_subplots(
            rows = 3, 
            cols = 1,
            subplot_titles = ("Nike", "VF Corporation", "Ralph Lauren")
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
            title_text = 'Stock Price',
            row = 1,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Stock Price',
            row = 2,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Stock Price',
            row = 3,
            col = 1
        )

        fig.update_xaxes(
            title_text = 'Date',
            row = 3,
            col = 1
        )

        fig.update_layout(title_text = 'Moving Average')
        st.plotly_chart(fig, use_container_width = True)

    with tc2:
        #Market Capitalization
        nke['Total Traded'] = nke['Adj Close'] * nke['Volume']
        vfc['Total Traded'] = vfc['Adj Close'] * vfc['Volume']
        rl['Total Traded'] = rl['Adj Close'] * rl['Volume']

        x1 = nke.index.values
        x2 = vfc.index.values
        x3 = rl.index.values

        y1 = nke['Total Traded'].values
        y2 = vfc['Total Traded'].values
        y3 = rl['Total Traded'].values

        fig = make_subplots(
            rows = 3, 
            cols = 1,
            subplot_titles = ("Nike", "VF Corporation", "Ralph Lauren")
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
            title_text = 'Total Money Traded',
            row = 1,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Total Money Traded',
            row = 2,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Total Money Traded',
            row = 3,
            col = 1
        )

        fig.update_xaxes(
            title_text = 'Date',
            row = 3,
            col = 1
        )

        fig.update_layout(title_text = 'Market Capitalization Approximate')
        st.plotly_chart(fig, use_container_width = True)
    
    #OHLC
    st.subheader('Click the companys button to see its OHLC graph')
    nke_button = st.button("Nike")
    vfc_button = st.button("VF Corporation")
    rl_button = st.button("Ralph Lauren")

    if nke_button:

        x = nke.index.values
        y1 = nke['Open'].values
        y2 = nke['High'].values
        y3 = nke['Low'].values
        y4 = nke['Close'].values

        fig = go.Figure(data=go.Ohlc(x = x, open = y1, high = y2, low = y3, close = y4))
        st.plotly_chart(fig, use_container_width = True)
    
    if vfc_button:

        x = vfc.index.values
        y1 = vfc['Open'].values
        y2 = vfc['High'].values
        y3 = vfc['Low'].values
        y4 = vfc['Close'].values

        fig = go.Figure(data=go.Ohlc(x = x, open = y1, high = y2, low = y3, close = y4))
        st.plotly_chart(fig, use_container_width = True)

    if rl_button:

        x = rl.index.values
        y1 = rl['Open'].values
        y2 = rl['High'].values
        y3 = rl['Low'].values
        y4 = rl['Close'].values

        fig = go.Figure(data=go.Ohlc(x = x, open = y1, high = y2, low = y3, close = y4))
        st.plotly_chart(fig, use_container_width = True)

#Restaurants
with tab3:
    tc1, tc2 = st.columns(2)

    with tc1:
        #Moving Average
        dpz['Mov Av 80'] = dpz['Adj Close'].rolling(80).mean()
        mcd['Mov Av 80'] = mcd['Adj Close'].rolling(80).mean()
        sbux['Mov Av 80'] = sbux['Adj Close'].rolling(80).mean()

        x1 = dpz.index.values
        x2 = mcd.index.values
        x3 = sbux.index.values

        y1 = dpz['Mov Av 80'].values
        y2 = mcd['Mov Av 80'].values
        y3 = sbux['Mov Av 80'].values

        fig = make_subplots(
            rows = 3, 
            cols = 1,
            subplot_titles = ("Dominos Pizza", "McDonalds Corp", "Starbucks")
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
            title_text = 'Stock Price',
            row = 1,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Stock Price',
            row = 2,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Stock Price',
            row = 3,
            col = 1
        )

        fig.update_xaxes(
            title_text = 'Date',
            row = 3,
            col = 1
        )

        fig.update_layout(title_text = 'Moving Average')
        st.plotly_chart(fig, use_container_width = True)

    with tc2:
        #Market Capitalization
        dpz['Total Traded'] = dpz['Adj Close'] * dpz['Volume']
        mcd['Total Traded'] = mcd['Adj Close'] * mcd['Volume']
        sbux['Total Traded'] = sbux['Adj Close'] * sbux['Volume']

        x1 = dpz.index.values
        x2 = mcd.index.values
        x3 = sbux.index.values

        y1 = dpz['Total Traded'].values
        y2 = mcd['Total Traded'].values
        y3 = sbux['Total Traded'].values

        fig = make_subplots(
            rows = 3, 
            cols = 1,
            subplot_titles = ("Dominos Pizza", "McDonalds Corp", "Starbucks")
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
            title_text = 'Total Money Traded',
            row = 1,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Total Money Traded',
            row = 2,
            col = 1
        )

        fig.update_yaxes(
            title_text = 'Total Money Traded',
            row = 3,
            col = 1
        )

        fig.update_xaxes(
            title_text = 'Date',
            row = 3,
            col = 1
        )

        fig.update_layout(title_text = 'Market Capitalization Approximate')
        st.plotly_chart(fig, use_container_width = True)
    
    #OHLC
    st.subheader('Click the companys button to see its OHLC graph')
    dpz_button = st.button("Dominos Pizza")
    mcd_button = st.button("McDonalds Corp")
    sbux_button = st.button("Starbucks")

    if dpz_button:

        x = dpz.index.values
        y1 = dpz['Open'].values
        y2 = dpz['High'].values
        y3 = dpz['Low'].values
        y4 = dpz['Close'].values

        fig = go.Figure(data=go.Ohlc(x = x, open = y1, high = y2, low = y3, close = y4))
        st.plotly_chart(fig, use_container_width = True)
    
    if mcd_button:

        x = mcd.index.values
        y1 = mcd['Open'].values
        y2 = mcd['High'].values
        y3 = mcd['Low'].values
        y4 = mcd['Close'].values

        fig = go.Figure(data=go.Ohlc(x = x, open = y1, high = y2, low = y3, close = y4))
        st.plotly_chart(fig, use_container_width = True)

    if sbux_button:

        x = sbux.index.values
        y1 = sbux['Open'].values
        y2 = sbux['High'].values
        y3 = sbux['Low'].values
        y4 = sbux['Close'].values

        fig = go.Figure(data=go.Ohlc(x = x, open = y1, high = y2, low = y3, close = y4))
        st.plotly_chart(fig, use_container_width = True)