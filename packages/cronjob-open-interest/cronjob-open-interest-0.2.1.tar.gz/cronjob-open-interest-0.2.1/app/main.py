import datetime as dt
from decouple import config
from pymongo import MongoClient

from radar_mongodb import QueryManager


def main():
    now = dt.datetime.now(tz = dt.timezone.utc)
    query_manager = QueryManager(
        db=MongoClient(config("MONGODB_URI")).get_default_database(),
        cboe_collection_name=config("CBOE_COLLECTION_NAME"),
        spot_collection_name=config("SPOT_COLLECTION_NAME"),
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
