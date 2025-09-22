import pandas as pd
import talib

def add_b_engulf(df):
    df['b_engulf'] = talib.CDLENGULFING(df['open'],df['high'], df['low'], df['close'])
    return df



pattern = {
    'eng': add_b_engulf
}