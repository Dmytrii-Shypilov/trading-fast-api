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
    print('COINNNNNS')
    print(body)
    data = await binance_client.get_symbol_traded_pairs(quote=body.quote)
    filtered_pairs = await binance_client.filter_symbol_by_volume_and_change(symbols=data, volume=body.volume, change=body.change)
    pairs_df = await binance_client.get_pairs_klines_data(list=filtered_pairs, interval=body.frame)
  
    # filter by uptrend if required
    if body.trend['uptrend']:
        pairs_df = indicators_manager.filter_coins_by_trend(pairs_df)
    result  = await indicators_manager.assign_pattern_signals(pairs_list=pairs_df, signals=body.indicators)
    
    print(len(data))
    print(len(filtered_pairs))
    print(len(pairs_df))
    
    response = []
    for idx, symb_df in enumerate(result):
       res =  transform_data_to_response(pairs_data=filtered_pairs[idx], indicators=body.indicators, df=symb_df)
       response.append(res)
       
    return response
  
    
