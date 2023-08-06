from pymongo.database import Database
from typing import TypedDict, List, Optional
import datetime as dt


class CBOEDocument(TypedDict):
    option: str
    bid: float
    bid_size: float
    ask: float
    ask_size: float
    iv: float
    open_interest: float
    volume: float
    delta: float
    gamma: float
    theta: float
    rho: float
    vega: float
    theo: float
    change: float
    open: float
    high: float
    low: float
    tick: str
    last_trade_price: float
    last_trade_time: dt.datetime
    percent_change: float
    prev_day_close: float


class CBOEQueries:
    def __init__(self, db: Database, collection_name: str):
        self.collection_name = collection_name
        self.collection = db["radar-cboe"]

    def insert_many(self, documents: List[CBOEDocument], now: Optional[dt.datetime] = None):
        if now is None:
            now = dt.datetime.now(dt.timezone.utc)
        row_date = dt.datetime(
            year = now.year,
            month = now.month,
            day = now.day,
            hour = now.hour,
            minute = (now.minute // 5) * 5,
            second = 0
        )
        for i in range(len(documents)):
            documents[i]["row_date"] = row_date
        return self.collection.insert_many(documents)