# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.utils.project import get_project_settings

from items import CardItem, SearchItem
from pymongo import MongoClient


class ScraperPipeline(object):
    def __init__(self):
        """
        Initializes Redis connection
        """
        mongo_connection_string = get_project_settings().get("MONGO_CONNECTION_STRING")
        # Mongo client
        self.client = MongoClient(mongo_connection_string)
        # Create Mongo database called 'mtg', with a collection (table) of results
        self.db = self.client.mtg.results

    def process_item(self, item, spider):
        """
        Save results to Mongo. We could process either a SearchItem or a Carditem
        """
        if isinstance(item, SearchItem):
            # Create initial doc if it doesnt exist
            self.db.find_one_and_update(
                {"_id": item.get("search_id")},
                {
                    "$setOnInsert": {
                        "datetime": item.get("datetime"),
                        "search_term": item.get("search_term"),
                        "results": {"Luckshack": [], "SATopDecked": []},
                    }
                },
                upsert=True,
            )

        if isinstance(item, CardItem):
            # Push additional search results onto list
            self.db.find_one_and_update(
                {"_id": item.get("search_id")},
                {
                    "$push": {
                        f"results.{item.get('store')}": {
                            "name": item.get("name"),
                            "price": item.get("price"),
                            "image_url": item.get("image_url"),
                        }
                    }
                },
                upsert=True,
            )

        return item
