import pandas as pd
import talib
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


class IndicatorsManager:
    # dynamic method dispatch
    def __init__(self):
        self.registry = {
            'engulfing': self.add_engulfing,
            'rsi': self.add_rsi,
            'dema': self.add_dema
        }
    def add_pattern_signals_to_df(self,df, signals: list):
        for signal in signals:
            self.registry[signal](df)
        
        
    def define_uptrend_by_lows(self, df):
        prices = df['close'].values
        peaks, _ = find_peaks(-prices, distance=10)

        # Ensure at least two peaks exist
        if len(peaks) < 2:
            return False  # Not enough peaks to determine trend
       
        # Get the last two peaks
        last_two_peaks = peaks[-2:]  # Last two lows (if available)
      
        # no change of character (no new lower low)
        no_choch = prices[-1] > prices[last_two_peaks[-1]]
        # Compare the last two peak values
        # and prices[last_three_peaks[-2]] > prices[last_three_peaks[-3]]:
        if len(last_two_peaks) == 2 and no_choch and prices[last_two_peaks[-1]] > prices[last_two_peaks[-2]]:
            # plt.figure(figsize=(12,6))
            # plt.plot(df.index, df['close'], label="Close Price", linewidth=2)
            # plt.scatter(df.index[last_two_peaks], df['close'].iloc[last_two_peaks], color="green",
            #             marker="o", s=80, label="Detected Lows", zorder=5)

            # if len(last_two_peaks) >= 2:
            #     last_lows_idx = last_two_peaks[-2:]
            #     plt.scatter(df.index[last_lows_idx], df['close'].iloc[last_lows_idx],
            #                 color="red", marker="D", s=120, label="Last 3 Lows", zorder=6)
            #     plt.plot(df.index[last_lows_idx], df['close'].iloc[last_lows_idx],
            #             color="orange", linestyle="--", linewidth=2, label="Trendline", zorder=4)

            # plt.title("Close Price with Detected Swing Lows")
            # plt.xlabel("Time")
            # plt.ylabel("Price")
            # plt.legend()
            # plt.grid(True)
            # plt.tight_layout()
            # plt.show()
            return True  # Uptrend confirmed
        return False  # No clear uptrend
    
    
    def define_resistance_breakout(self):
        pass

    
    def add_engulfing(self, df):
        df['eng'] = talib.CDLENGULFING(df['open'],df['high'], df['low'], df['close'])

    def add_rsi(self, df):
      df['rsi'] = talib.RSI(df['close'], timeperiod=9)
      
    def add_dema(self, df):
       
        df['ema7']= talib.EMA(df['close'], timeperiod=7)
        df['ema25'] = talib.EMA(df['close'], timeperiod=25)
        df['dema'] = round(((df['ema7'] - df['ema25'])/df['ema25'])*100, 2)
        
    