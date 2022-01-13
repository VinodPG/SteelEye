from fastapi import FastAPI
from database import database, trades

import datetime as dt
from typing import Optional, List
from pydantic import BaseModel, Field


class TradeDetails(BaseModel): 
    buySellIndicator: str = Field(
        description="A value of BUY for buys, SELL for sells." 
    )
    price: float = Field(
        description="The price of the Trade."
    )
    quantity: int = Field(
        description="The amount of units traded."
    )
    

class Trade(BaseModel):
    asset_class: Optional[str] = Field(
        alias="assetClass",
        default=None,
        description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc"
    )
    counterparty: Optional[str] = Field( default=None,
        description="The counterparty the trade was executed with. May not always be available" 
    )
    instrument_id: str = Field(
        alias="instrumentId",
        description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc"
    )
    instrument_name: str = Field( alias="instrumentName",
        description="The name of the instrument traded."
    )
    trade_date_time: dt.datetime = Field( alias="tradeDateTime",
        description="The date-time the Trade was executed"
    )
    trade_details: TradeDetails = Field(
        alias="tradeDetails",
        description="The details of the trade, i.e. price, quantity"
    )
    trade_id: str = Field( alias="tradeId",
        default=None,
        description="The unique ID of the trade" )
    trader: str = Field(description="The name of the Trader")


app = FastAPI()


@app.on_event("startup")
async def database_connect():
    await database.connect()

@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()

#Get list of trades
@app.get("/trades/")
async def get():
    query = trades.select()
    return await database.fetch_all(query)

#Get trade based on trade ids
@app.get("/trades/{trade_id}")
async def get(trade_id):
    query = trades.select().where(trades.columns.trade_id==trade_id)
    return await database.fetch_all(query)

#Read trade details based on filter counterparty,counterparty,instrumentName,trader
@app.get("/read_trades")
async def read_trades(counterparty: Optional[str] = None, instrument_id: Optional[str] = None,
                instrumentName: Optional[str] = None, trader: Optional[str] = None):
    query = trades.select()
    if counterparty:
        query = query.filter(trades.columns.counterparty==counterparty)
    if instrument_id:
        query = query.filter(trades.columns.instrument_id==instrument_id)
    if instrumentName:
        query = query.filter(trades.columns.instrument_name==instrumentName)
    if trader:
        query = query.filter(trades.columns.trader==trader)
    return await database.fetch_all(query)

#Write trade details to DB
@app.post("/trades/")
async def post(trade: Trade):
    print(trade.json())
    query = trades.insert().values(
                            asset_class=trade.asset_class, 
                            counterparty=trade.counterparty, 
                            instrument_id=trade.instrument_id,
                            instrument_name=trade.instrument_name,
                            trade_date_time=trade.trade_date_time,
                            buySellIndicator=trade.trade_details.buySellIndicator,
                            price=trade.trade_details.price,
                            quantity=trade.trade_details.quantity,
                            trade_id=trade.trade_id,
                            trader=trade.trader)
    last_record_id = await database.execute(query)
    return {**trade.dict(), "id": last_record_id}
