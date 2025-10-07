import pandas as pd
import talib
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from app.services.async_manager import AsyncManager


class IndicatorsManager:
    # dynamic method dispatch
    def __init__(self):
        self.registry = {
            'eng': self.add_engulfing,
            'rsi': self.add_rsi,
            'dema': self.add_dema
        }

    async def add_pattern_signals_to_df(self, df, signals: list):   
        for signal in signals:
         await self.registry[signal](df)
        return df
    
    async def assign_pattern_signals(self, pairs_list: list, signals: list):
        asyncer = AsyncManager()

        for pair in pairs_list:
            await asyncer.add_async_operation(self.add_pattern_signals_to_df(pair, signals))
        result = await asyncer.get_results()
        return result

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
    
    def filter_coins_by_trend(self, df_list):
        filtered = []
        for df in df_list:
           is_uptrend = self.define_uptrend_by_lows(df=df)
           if is_uptrend:
               filtered.append(df)
        return filtered

    async def define_resistance_breakout(self):
        pass

    async def add_engulfing(self, df):
        df['eng'] = talib.CDLENGULFING(
            df['open'], df['high'], df['low'], df['close'])

    async def add_rsi(self, df):
        df['rsi'] = talib.RSI(df['close'], timeperiod=9)

    async def add_dema(self, df):

        df['ema7'] = talib.EMA(df['close'], timeperiod=7)
        df['ema25'] = talib.EMA(df['close'], timeperiod=25)
        df['dema'] = round(((df['ema7'] - df['ema25'])/df['ema25'])*100, 2)


indicators_manager = IndicatorsManager()