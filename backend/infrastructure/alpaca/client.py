from __future__ import annotations
from alpaca.trading.client import TradingClient
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.historical.stock import StockHistoricalDataClient

class AlpacaClients:
    def __init__(self, api_key: str, secret: str, paper: bool = True):
        self.trading = TradingClient(api_key, secret, paper=paper)
        self.options_data = OptionHistoricalDataClient(api_key, secret)
        self.stock_data = StockHistoricalDataClient(api_key, secret)
