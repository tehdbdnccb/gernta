from __future__ import annotations
import statistics
import httpx
from application.market.features import MarketFeatures

class AlpacaMarketDataProvider:
    def __init__(self, api_key: str, secret: str, paper: bool = True):
        self.headers={"APCA-API-KEY-ID":api_key,"APCA-API-SECRET-KEY":secret}
        self.base="https://data.alpaca.markets"
    async def get_features(self, symbol: str) -> MarketFeatures:
        async with httpx.AsyncClient(timeout=10) as client:
            r=await client.get(f"{self.base}/v2/stocks/{symbol}/bars",headers=self.headers,params={"timeframe":"1Day","limit":30,"feed":"iex"})
            r.raise_for_status(); bars=r.json().get("bars",[])
        closes=[float(x["c"]) for x in bars if float(x["c"])>0]
        if not closes: raise ValueError(f"No market data for {symbol}")
        price=closes[-1]
        trend=((price/closes[-6])-1)*100 if len(closes)>=6 else 0.0
        momentum=((price/closes[-2])-1)*100 if len(closes)>=2 else 0.0
        returns=[(closes[i]/closes[i-1]-1)*100 for i in range(1,len(closes))]
        vol=statistics.pstdev(returns)*(252**0.5) if len(returns)>1 else 0.0
        return MarketFeatures(price,trend,vol,momentum)
