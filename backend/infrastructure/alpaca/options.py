from __future__ import annotations
from datetime import date, timedelta
import httpx
from domain.options import OptionContract

class AlpacaOptionProvider:
    def __init__(self, api_key: str, secret: str):
        self.headers={"APCA-API-KEY-ID":api_key,"APCA-API-SECRET-KEY":secret}
        self.trade_base="https://paper-api.alpaca.markets"
        self.data_base="https://data.alpaca.markets"
    async def get_chain(self, symbol: str) -> list[OptionContract]:
        today=date.today(); expiry=today+timedelta(days=60)
        async with httpx.AsyncClient(timeout=15) as client:
            r=await client.get(f"{self.trade_base}/v2/options/contracts",headers=self.headers,params={"underlying_symbols":symbol,"status":"active","expiration_date_gte":today.isoformat(),"expiration_date_lte":expiry.isoformat(),"limit":10000})
            r.raise_for_status(); contracts=r.json().get("option_contracts",[])
            snap=await client.get(f"{self.data_base}/v1beta1/options/snapshots/{symbol}",headers=self.headers,params={"feed":"indicative","limit":1000})
            snapshots=snap.json().get("snapshots",{}) if snap.is_success else {}
        result=[]
        for c in contracts:
            s=str(c["symbol"]); typ=str(c["type"]).lower(); q=snapshots.get(s,{})
            quote=q.get("latestQuote",{})
            bid=float(quote.get("bp") or 0); ask=float(quote.get("ap") or 0)
            greeks=q.get("greeks",{})
            result.append(OptionContract(s,str(c["underlying_symbol"]),date.fromisoformat(str(c["expiration_date"])),float(c["strike_price"]),typ,bid,ask,(bid+ask)/2 if ask else 0.0,float(q.get("impliedVolatility")) if q.get("impliedVolatility") is not None else None,float(greeks.get("delta")) if greeks.get("delta") is not None else None))
        return result
