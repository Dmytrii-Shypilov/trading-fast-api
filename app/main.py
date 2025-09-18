from  fastapi import FastAPI
from binance import AsyncClient

from .services.client import binance_client

API  = 'W4G23O8koOoYXwoG6wHM1LJTEbaHHzm9uiLxjeToi10Owyanev1DipEwkTFvvzxe'

client = AsyncClient(api_key=API)

app = FastAPI()


@app.get("/")
async def home():
    data = await binance_client.fetch_kline_data('BTCUSDT')
    return data