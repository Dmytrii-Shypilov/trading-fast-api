from binance import Client
import pandas as pd
import talib
import matplotlib.pyplot as plt
import mplfinance as mpf

def plot_candlesticks(df, title="Candlestick Chart"):
    """
    Plots candlesticks using mplfinance.
    df must have columns: ['open','high','low','close'] and DateTime index.
    """
    mpf.plot(
        df,
        type='candle',
        style='charles',  # you can try 'binance', 'yahoo', 'classic'
        title=title,
        ylabel='Price',
        volume=True,      # show volume below chart
        mav=(5, 10, 20),  # moving averages
        figratio=(16,9),
        figscale=1.2
    )
    

def add_b_engulf(df):
    df['b_engulf'] = talib.CDLENGULFING(df['open'],df['high'], df['low'], df['close'])
    return df

def convert_to_dataframe(data):
    df = pd.DataFrame(data, columns=[
                      'timestamp', 'open', 'high', 'low', 'close', 'volume', '_1', '_2', '_3', '_4', '_5', '_6'])
    df = df[['timestamp', 'open', 'high',
             'low', 'close', 'volume']].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    df.set_index('timestamp', inplace=True)

    return df


client = Client(
    api_key='W4G23O8koOoYXwoG6wHM1LJTEbaHHzm9uiLxjeToi10Owyanev1DipEwkTFvvzxe')


klines = client.get_historical_klines(
    interval='5m', symbol='ETHUSDT', limit=40)
df = convert_to_dataframe(klines)
pat = add_b_engulf(df)
print(df)
plot_candlesticks(df)
