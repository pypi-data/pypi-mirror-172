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
        open_interest_collection_name=config("OPEN_INTEREST_COLLECTION_NAME"),
    )
    query_manager.open_interest.insert(now)
    print("success")


if __name__ == "__main__":
    main()
