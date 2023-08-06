import datetime as dt
from decouple import config
from pymongo import MongoClient
import pandas as pd

from cboe_extractor import CBOEExtractor
from radar_mongodb import QueryManager


def main():
    now = dt.datetime.now(tz = dt.timezone.utc)
    query_manager = QueryManager(
        db=MongoClient(config("MONGODB_URI")).get_default_database(),
        cboe_collection_name=config("CBOE_COLLECTION_NAME"),
        spot_collection_name=config("SPOT_COLLECTION_NAME"),
    )
    cboe_extractor = CBOEExtractor(cboe_host=config("CBOE_HOST"))
    df: pd.DataFrame = cboe_extractor.to_dataframe()
    current_price: float = cboe_extractor.get_current_price()
    df.dropna(axis=0, inplace=True)
    query_manager.cboe_queries.insert_many(
        documents=df.to_dict(orient="records"), 
        now = now
    )
    query_manager.spot_queries.insert_many(
        document={
            "current_price": current_price
        },
        now = now
    )
    print("success")


if __name__ == "__main__":
    main()
