#!/usr/bin/env python3

import json
import time
import uuid
from subprocess import Popen, PIPE

import requests
from kafka import KafkaConsumer


def get_kafka_consumer():
    topic = "search"
    hosts = "172.20.0.3:29092,172.20.0.4:39092"
    group_id = "search-group"

    return KafkaConsumer(
        topic,
        bootstrap_servers=hosts,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )


if __name__ == "__main__":
    print("Starting Kafka Consumer")
    consumer = get_kafka_consumer()

    spiders = [
        "topdecked",
        "luckshack",
        "d20battleground",
        "battlewizards",
    ]

    # Loops forever, consumer is an iterator
    for message in consumer:
        search_term = message.value["search"]
        print(f"Scraping: {search_term}")
        # Share primary key for this search
        search_id = str(uuid.uuid4())

        for spider in spiders:
            print(f"Fetching {spider}...")
            requests.post(
                "http://scrapyd:6800/schedule.json",
                data={"project": "default", "spider": spider, "uuid": search_id, "search_term": search_term},
            )

        time.sleep(5)
        print("Waiting for more...")
