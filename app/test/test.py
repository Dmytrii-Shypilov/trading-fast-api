from binance import Client
import pandas as pd
import talib
import matplotlib.pyplot as plt
import mplfinance as mpf
from scipy.signal import find_peaks

# two last lows
# 1h - 12 distance
# 5m - 6 distnce

class IndicatorsManager:
    # dynamic method dispatch
    def __init__(self):
        self.registry = {
            'engulfing': self.add_engulfing,
            'rsi': self.add_rsi
        }
        
    def define_uptrend_by_lows(self, df, distance=6, plot=True, noise_threshold=0.0):
        """
        Detect swing lows, optionally plot, and return (uptrend_bool, lows_indices).
        - df: DataFrame with a 'close' column and any index (datetime or integer).
        - distance: min samples between detected lows.
        - noise_threshold: fractional minimum increase between lows (e.g. 0.003 for 0.3%).
        """
        prices = df['close'].values
        lows, _ = find_peaks(prices, distance=distance)

        # Plot (correct x alignment)
        if plot:
            plt.figure(figsize=(12,6))
            plt.plot(df.index, df['close'], label="Close Price", linewidth=2)
            plt.scatter(df.index[lows], df['close'].iloc[lows], color="green",
                        marker="o", s=80, label="Detected Lows", zorder=5)

            if len(lows) >= 2:
                last_lows_idx = lows[-2:]
                plt.scatter(df.index[last_lows_idx], df['close'].iloc[last_lows_idx],
                            color="red", marker="D", s=120, label="Last 3 Lows", zorder=6)
                plt.plot(df.index[last_lows_idx], df['close'].iloc[last_lows_idx],
                        color="orange", linestyle="--", linewidth=2, label="Trendline", zorder=4)

            plt.title("Close Price with Detected Swing Lows")
            plt.xlabel("Time")
            plt.ylabel("Price")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
    def add_pattern_signals_to_df(self,df, signals: list):
        for signal in signals:
            self.registry[signal](df)
        
        

    def define_resistance_breakout(self):
        pass

    
    def add_engulfing(self, df):
        df['eng'] = talib.CDLENGULFING(df['open'],df['high'], df['low'], df['close'])

    def add_rsi(self, df):
      df['rsi'] = talib.RSI(df['close'], timeperiod=9)

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


ind_manager = IndicatorsManager()
indicators = ['engulfing', 'rsi']

client = Client(
    api_key='W4G23O8koOoYXwoG6wHM1LJTEbaHHzm9uiLxjeToi10Owyanev1DipEwkTFvvzxe')


klines = client.get_historical_klines(
    interval='5m', symbol='ACHUSDT', limit=40)
df = convert_to_dataframe(klines)

print(ind_manager.define_uptrend_by_lows(df))
# ind_manager.add_pattern_signals_to_df(df, indicators)
# print(df)
# pat = add_b_engulf(df)
# print(df)
# plot_candlesticks(df)
