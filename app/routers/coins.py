from fastapi import APIRouter, HTTPException, Response, Request
from app.services.client import binance_client


coins_router = APIRouter(prefix='', tags=['Fecthing Coins'])


@coins_router.get('/coins')
async def get_coins(pair: str, volume: int, volatility: int, growth: int):
    print(pair, volume, volatility, growth)
    return [{'pair': 'USDTBTC'},{'pair': 'USDTBTC'}, {'pair': 'USDTBTC'}]