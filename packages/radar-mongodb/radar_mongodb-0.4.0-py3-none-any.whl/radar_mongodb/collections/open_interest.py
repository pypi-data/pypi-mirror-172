from pymongo.database import Database
from typing import TypedDict, Optional
import datetime as dt
from enum import Enum


class OptionType(str, Enum):
    P: str = "P"
    C: str = "C"


class OpenInterestDocument(TypedDict):
    open_interest: float
    option_type: OptionType
    strike: str


class OpenInterestQueries:
    def __init__(self, db: Database, collection_name: str):
        self.collection_name = collection_name
        self.open_interest_collection = db["radar-open-interest"]
        self.cboe_collection = db["radar-cboe"]

    def insert(self, now: Optional[dt.datetime] = None):
        if now is None:
            now = dt.datetime.now(dt.timezone.utc)
        now = dt.datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=0,
            second=0,
        )
        result = self.cboe_collection.aggregate(
            [
                {
                    "$match": {"row_date": now - dt.timedelta(seconds=60 * 60)},
                },
                {
                    "$project": {
                        "option_type": {"$substr": ["$option", 9, 1]},
                        "strike": {"$substr": ["$option", 11, 4]},
                        "open_interest": True,
                    }
                },
                {"$match": {"option_type": {"$in": ["C", "P"]}}},
                {
                    "$group": {
                        "_id": {"option_type": "$option_type", "strike": "$strike"},
                        "open_interest": {"$sum": "$open_interest"},
                    }
                },
                {
                    "$project": {
                        "_id": False,
                        "option_type": "$_id.option_type",
                        "strike": "$_id.strike",
                        "open_interest": True,
                    }
                },
                {
                    "$sort": {
                        "strike": 1,
                        "option_type": -1,
                    }
                },
            ]
        )
        documents = list(result)
        if len(documents) != 0:
            for i in range(len(documents)):
                documents[i]["datetime"] = dt.datetime(
                    year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0
                )
            self.open_interest_collection.insert_many(documents)
        else:
            print("No hay datos")

    def find(self, date: dt.date):
        return list(self.open_interest_collection.find(
            filter = {
                "datetime": dt.datetime.combine(
                    date = date,
                    time = dt.time.min
                )
            },
            projection = {
                "_id": False
            }
        ))