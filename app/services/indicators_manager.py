import pandas as pd
import talib
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


class IndicatorsManager:
    # dynamic method dispatch
    def __init__(self):
        self.registry = {
            'engulfing': self.add_engulfing,
            'rsi': self.add_rsi
        }
    def add_pattern_signals_to_df(self,df, signals: list):
        for signal in signals:
            self.registry[signal](df)
        
        
    def define_uptrend_by_lows(self, df):
        prices = df['close'].values
        peaks, _ = find_peaks(-prices, distance=6)

        # Ensure at least two peaks exist
        if len(peaks) < 3:
            return False  # Not enough peaks to determine trend

        # Get the last two peaks
        last_three_peaks = peaks[-3:]  # Last three peaks (if available)
        no_choch = prices[-1] > prices[last_three_peaks[-2]]
        # Compare the last two peak values
        # and prices[last_three_peaks[-2]] > prices[last_three_peaks[-3]]:
        if len(last_three_peaks) == 3 and no_choch and prices[last_three_peaks[-1]] > prices[last_three_peaks[-2]]:
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
        