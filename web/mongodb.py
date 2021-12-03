import os

from pymongo import MongoClient
from flask import g


class Mongo:
    """A jank attempt at abstracting away the db"""

    def get_client(self):
        connection_string = os.getenv("MONGO_CONNECTION_STRING")
        self.client = MongoClient(connection_string)

    def get_collection(self):
        # Create if not exists and return Mongo database called 'mtg', with a collection (table) of results
        self.get_client()
        return self.client.mtg.results

    def close(self):
        self.client.close()


def get_mongo_db():
    if "mongo_db" not in g:
        g.db = Mongo()
    return g.db


def close_db(e=None):
    db = g.pop("mongo_db", None)

    if db is not None:
        db.close()
