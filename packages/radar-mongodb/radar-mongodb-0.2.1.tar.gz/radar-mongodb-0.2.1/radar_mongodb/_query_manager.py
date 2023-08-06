from pymongo.database import Database

from .collections.cboe import CBOEQueries
from .collections.spot import SpotQueries


class QueryManager:
    def __init__(self, db: Database, cboe_collection_name: str, spot_collection_name: str):
        self.db = db
        self.cboe_queries = CBOEQueries(db=db, collection_name=cboe_collection_name)
        self.spot_queries = SpotQueries(db=db, collection_name=spot_collection_name)