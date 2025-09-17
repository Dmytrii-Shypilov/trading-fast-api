from binance import AsyncClient
from pattern_manager import PaternManager

API  = 'W4G23O8koOoYXwoG6wHM1LJTEbaHHzm9uiLxjeToi10Owyanev1DipEwkTFvvzxe'


class BinanceClient:
    client = AsyncClient(api_key=API)
    pattern_manager = PaternManager()

    def fetch_kline_data(self, interval):
        pass

    def get_symbol_traded_pairs(self):
        pass

    def fetch_order_book(self):
        pass