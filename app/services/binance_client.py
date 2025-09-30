from binance import AsyncClient, Client
from .indicators_manager import IndicatorsManager
from .async_manager import AsyncManager
import pandas as pd



API = 'W4G23O8koOoYXwoG6wHM1LJTEbaHHzm9uiLxjeToi10Owyanev1DipEwkTFvvzxe'


class BinanceClient:
    def __init__(self):
        self.client = AsyncClient(api_key=API)
        self.indicator = IndicatorsManager()
        self.asyncer = AsyncManager()

    # converts klines data to dataframe

    def convert_to_dataframe(self, data):
        df = pd.DataFrame(data, columns=[
                          'timestamp', 'open', 'high', 'low', 'close', 'volume', '_1', '_2', '_3', '_4', '_5', '_6'])

        df = df[['timestamp', 'open', 'high',
                 'low', 'close', 'volume']].astype(float)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df

    # fetches symbol traded pairs

    async def get_symbol_traded_pairs(self, quote: str):
        exchange_info = await self.client.get_exchange_info()
        symbols = exchange_info['symbols']
        traded_pairs = [symbol['symbol'] for symbol in symbols if symbol['quoteAsset']
                        == quote and symbol['status'] == 'TRADING']
        return traded_pairs

    async def filter_symbol_by_volume_and_change(self, symbols: list,  volume: int,  change: float):
        all_tickers = await self.client.get_ticker()
        # print([ticker for ticker in all_tickers if ticker['symbol'] == "XPLUSDT"][0])
        filtered = [{'quote': ticker['symbol'], 'volume': ticker['quoteVolume'], 'change': ticker['priceChangePercent'], 'indicators': []} for ticker in all_tickers if ticker['symbol'] in symbols and float(
            ticker['quoteVolume']) >= volume and float(ticker['priceChangePercent']) >= change]
        
        return filtered

    # fetch single pair candlestick data
    async def fetch_kline_data(self, symbol, interval='5m'):
        try:
            klines = await self.client.get_historical_klines(symbol=symbol, interval=interval)
            data_frame = self.convert_to_dataframe(klines)
            # analyze data OR DO IT SEPARATELY IN PATTERNER
            # ----> inside patterner
            # await asyncer.add_async_op(self.patterner.add_patterns())
            # kline = await asyncer.get_results()
            return data_frame
        except Exception as e:
            print(f"Exception fetching coin {symbol} from Binance API")

    # fetch multiple pairs candlestick data

    async def get_pairs_klines_data(self, list):
        for pair in list:
            await self.asyncer.add_async_operation(self.fetch_kline_data(symbol=pair))
        data = await self.asyncer.get_results()
        return data

    def fetch_order_book(self):
        pass


binance_client = BinanceClient()

# async def init_client(self):
#     """Create the async Binance client once."""
#     if self.client is None:
#         self.client = await AsyncClient.create(api_key=API)

# async def close_client(self):
#     """Close the client (should be done once, when app stops)."""
#     if self.client:
#         await self.client.close_connection()
#         self.client = None
