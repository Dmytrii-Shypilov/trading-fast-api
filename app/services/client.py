from binance import AsyncClient
from .pattern_manager import PatternManager
from .async_manager import AsyncManager

API  = 'W4G23O8koOoYXwoG6wHM1LJTEbaHHzm9uiLxjeToi10Owyanev1DipEwkTFvvzxe'


class BinanceClient:
    def __init__(self):
        self.client =  AsyncClient
        self.patterner = PatternManager()
        self.asyncer = AsyncManager()

    async def fetch_kline_data(self, symbol, interval='5m'):
        async_client = await self.client.create(api_key=API)
        klines = await async_client.get_historical_klines(symbol=symbol, interval=interval)
        return klines
    
    async def get_pairs_klines_data(self, list):
        for pair in list:
           await self.asyncer.add_async_operation(self.fetch_kline_data(symbol=pair))
        data = await self.asyncer.get_results()
        return data
            
        
    
    def get_symbol_traded_pairs(self):
        pass

    def fetch_order_book(self):
        pass

    


binance_client = BinanceClient()