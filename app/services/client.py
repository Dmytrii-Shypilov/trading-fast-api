from binance import AsyncClient
from .pattern_manager import PatternManager

API  = 'W4G23O8koOoYXwoG6wHM1LJTEbaHHzm9uiLxjeToi10Owyanev1DipEwkTFvvzxe'


class BinanceClient:
    client = AsyncClient(api_key=API)
    pattern_manager = PatternManager()

    def fetch_kline_data(self, symbol, interval='5m'):
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval)
        return klines
    def get_symbol_traded_pairs(self):
        pass

    def fetch_order_book(self):
        pass



binance_client = BinanceClient()