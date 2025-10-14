from fastapi import APIRouter, WebSocket
from app.services.binance_client import binance_client
from time import sleep


traded_pair_stream = APIRouter(prefix='', tags=['Streaming traded pairs'])

pairs = ['BTCUSDT', 'ETHUSDT']

@traded_pair_stream.websocket('/traded_stream')
async def stream_traded_data(websocket: WebSocket):
    await websocket.accept()
    for i in range(1,5):
        sleep(1)
        data = await binance_client.fetch_order_book(symbol='BTCUSDT')
        await websocket.send_json(data)