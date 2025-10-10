from fastapi import APIRouter
from app.services.binance_client import binance_client
from app.services.indicators_manager import indicators_manager
import matplotlib.pyplot as plt
import mplfinance as mpf

test_routes = APIRouter(prefix='', tags=['Testing route'])

@test_routes.get('/test')
async def test_route():
    data = await binance_client.get_symbol_traded_pairs(quote='USDT')
    filtered_pairs = await binance_client.filter_symbol_by_volume_and_change(symbols=data, volume=200000, change=0)
    pairs_df = await binance_client.get_pairs_klines_data(list=filtered_pairs, interval='1h')
    ind_df = await indicators_manager.assign_pattern_signals(pairs_list=pairs_df,signals=['eng'])
    
    res = []
    
    for df in ind_df:
        if df['eng'].iloc[-1] == 100:
            res.append(df)
            
    for df in res[:10]:
        mpf.plot(df.tail(), type='candle', style='charles', title='Candlestick Chart from DataFrame', volume=False)