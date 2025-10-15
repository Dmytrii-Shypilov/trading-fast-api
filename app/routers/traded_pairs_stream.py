from fastapi import APIRouter, WebSocket
from app.services.binance_client import binance_client
import json
from time import sleep


traded_pair_stream = APIRouter(prefix='', tags=['Streaming traded pairs'])

pairs = ['BTCUSDT', 'ETHUSDT']


@traded_pair_stream.websocket('/traded_stream')
async def stream_traded_data(websocket: WebSocket):
    await websocket.accept()
    request_data = await websocket.receive_text()
    request_coins = json.loads(request_data).get('pairsList')

    while True:

        data = await binance_client.get_traded_stream_data(pairs=request_coins)

        await websocket.send_json(data)
        sleep(1)
