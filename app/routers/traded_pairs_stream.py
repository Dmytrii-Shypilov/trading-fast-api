from fastapi import APIRouter, WebSocket
from app.services.binance_client import binance_client
from time import sleep


traded_pair_stream = APIRouter(prefix='', tags=['Streaming traded pairs'])

pairs = ['BTCUSDT', 'ETHUSDT']

@traded_pair_stream.websocket('/traded_stream')
async def stream_traded_data(websocket: WebSocket):
    await websocket.accept()

    data = await binance_client.get_traded_stream_data(pairs=pairs)
   
    await websocket.send_json(data)