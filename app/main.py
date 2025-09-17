from  fastapi import FastAPI
from binance import AsyncClient

API  = 'W4G23O8koOoYXwoG6wHM1LJTEbaHHzm9uiLxjeToi10Owyanev1DipEwkTFvvzxe'

client = AsyncClient(api_key=API)

app = FastAPI()


@app.get("/")
async def home():
    for i in range(10):
        print(i)
        data = await client.get_historical_klines('BTCUSDT', AsyncClient.KLINE_INTERVAL_5MINUTE, '1 day ago UTC')
    return 'stopped'