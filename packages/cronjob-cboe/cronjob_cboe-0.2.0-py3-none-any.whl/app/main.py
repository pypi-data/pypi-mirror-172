from decouple import config
from pymongo import MongoClient
import pandas as pd

from cboe_extractor import CBOEExtractor
from radar_mongodb import QueryManager


def main():
    query_manager = QueryManager(
        db=MongoClient(config("MONGODB_URI")).get_default_database(),
        cboe_collection_name=config("CBOE_COLLECTION_NAME"),
    )
    cboe_extractor = CBOEExtractor(cboe_host=config("CBOE_HOST"))
    df: pd.DataFrame = cboe_extractor.to_dataframe()
    df.dropna(axis=0, inplace=True)
    query_manager.cboe_queries.insert_many(documents=df.to_dict(orient="records"))
    print("success")


if __name__ == "__main__":
    main()
