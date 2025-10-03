from fastapi import APIRouter, HTTPException, Response, Request
from app.services.binance_client import binance_client
from app.services.indicators_manager import IndicatorsManager

coins_router = APIRouter(prefix='', tags=['Fetching Coins'])

ind_m = IndicatorsManager()

@coins_router.get('/coins')
async def get_coins(quote: str, volume: int, change: int):
    data = await binance_client.get_symbol_traded_pairs(quote=quote)
    result = await binance_client.filter_symbol_by_volume_and_change(symbols=data, volume=float(volume), change=float(change))
    # print(quote, volume, change)
    
    symbols = [pair['quote'] for pair in result]

    pairs = await binance_client.get_pairs_klines_data(symbols)
   
    print(f'{len(symbols)} : {len(pairs)}')
    coins = []
    # for idx, pair in enumerate(pairs):
    #     ind_m.add_dema(df=pair)
    #     # print(pair['dema'].iloc[-1])
    #     if pair['dema'].iloc[-1] > 0:
         
    #         coins.append([symbols[idx], pair['dema'].iloc[-1]])
    # print(coins)
    for idx, pair in enumerate(pairs):
        ind_m.add_dema(pair)
        res = ind_m.define_uptrend_by_lows(df=pair)
        if res == True:
            coins.append(symbols[idx])
            
       
    print(coins)
    
    return result