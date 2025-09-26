from fastapi import APIRouter, HTTPException, Response, Request
from app.services.binance_client import binance_client


coins_router = APIRouter(prefix='', tags=['Fetching Coins'])


@coins_router.get('/coins')
async def get_coins(quote: str, volume: int, change: int):
    data = await binance_client.get_symbol_traded_pairs(quote=quote)
    result = await binance_client.filter_symbol_by_volume_and_change(symbols=data, volume=float(volume), change=float(change))
    # print(quote, volume, change)
    return result