import json
import time
import uuid
from subprocess import Popen, PIPE

from kafka import KafkaConsumer


def get_kafka_consumer():
    topic = "search"
    host = "localhost"
    port = "29092"
    group_id = "search-group"

    return KafkaConsumer(
        topic,
        bootstrap_servers=[f"{host}:{port}"],
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )


if __name__ == "__main__":
    print("Starting Kafka Consumer")
    consumer = get_kafka_consumer()

    # Loops forever, consumer is an iterator
    for message in consumer:
        search_term = message.value["search"]
        print(f"Scraping: {search_term}")
        # Share primary key for this search
        search_id = str(uuid.uuid4())

        # Search Top decked
        topdecked_spider = Popen(
            [
                "scrapy",
                "crawl",
                "topdecked",
                "-a",
                f"search_term={search_term}",
                "-a",
                f"uuid={search_id}",
            ],
            stdout=PIPE,
        )
        topdecked_spider.wait()

        # Search Luckshack
        luckshack_spider = Popen(
            [
                "scrapy",
                "crawl",
                "luckshack",
                "-a",
                f"search_term={search_term}",
                "-a",
                f"uuid={search_id}",
            ],
            stdout=PIPE,
        )
        luckshack_spider.wait()

        # Search D20Battleground
        d20battleground_spider = Popen(
            [
                "scrapy",
                "crawl",
                "d20battleground",
                "-a",
                f"search_term={search_term}",
                "-a",
                f"uuid={search_id}",
            ],
            stdout=PIPE,
        )
        d20battleground_spider.wait()
        time.sleep(60)
        print("Waiting for more...")
