from fastapi import APIRouter, HTTPException, Response, Request
from app.services.binance_client import binance_client
from app.services.indicators_manager import indicators_manager
from app.services.helpers import transform_data_to_response
from pydantic import BaseModel

coins_router = APIRouter(prefix='', tags=['Fetching Coins'])


class RequestBody(BaseModel):
    quote: str
    volume: float
    frame: str
    change: float
    trend: dict
    indicators: list

@coins_router.post('/coins')
async def get_coins(body: RequestBody):
    data = await binance_client.get_symbol_traded_pairs(quote=body.quote)
    filtered_pairs = await binance_client.filter_symbol_by_volume_and_change(symbols=data, volume=body.volume, change=body.change)
    pairs_df = await binance_client.get_pairs_klines_data(list=filtered_pairs, interval=body.frame)
    result  = await indicators_manager.assign_pattern_signals(pairs_list=pairs_df, signals=body.indicators)
    print(body.indicators)
    print(data[0])
    print(filtered_pairs[0])
    print(result[0])
    print(len(result))
    
    response = []
    for idx, symb_df in enumerate(result):
       res =  transform_data_to_response(symbol=filtered_pairs[idx]['quote'], payload=body, df=symb_df)
       response.append(res)
    print(response[0])
    return response
    # # print(quote, volume, change)
    
    # symbols = [pair['quote'] for pair in result]

    # pairs = await binance_client.get_pairs_klines_data(symbols)
   
    # print(f'{len(symbols)} : {len(pairs)}')
    # coins = []
    # # for idx, pair in enumerate(pairs):
    # #     ind_m.add_dema(df=pair)
    # #     # print(pair['dema'].iloc[-1])
    # #     if pair['dema'].iloc[-1] > 0:
         
    # #         coins.append([symbols[idx], pair['dema'].iloc[-1]])
    # # print(coins)
    # for idx, pair in enumerate(pairs):
    #     ind_m.add_dema(pair)
    #     res = ind_m.define_uptrend_by_lows(df=pair)
    #     if res == True:
    #         coins.append(symbols[idx])
            
       
    # print(coins)
    
