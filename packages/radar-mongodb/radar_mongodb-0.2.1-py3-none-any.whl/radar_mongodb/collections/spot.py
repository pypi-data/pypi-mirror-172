from pymongo.database import Database
from typing import TypedDict
import datetime as dt


class SpotDocument(TypedDict):
    current_price: float


class SpotQueries:
    def __init__(self, db: Database, collection_name: str):
        self.collection_name = collection_name
        self.collection = db["radar-spot"]

    def insert_many(self, document: SpotDocument):
        now = dt.datetime.now(dt.timezone.utc)
        row_date = dt.datetime(
            year = now.year,
            month = now.month,
            day = now.day,
            hour = now.hour,
            minute = now.minute,
            second = 0
        )
        document["row_date"] = row_date
        return self.collection.insert_one(document)