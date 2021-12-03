#!/usr/bin/env python3

import json
import os
import time
import uuid
from subprocess import Popen, PIPE

import requests
from kafka import KafkaConsumer


def get_kafka_consumer():
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    topic = os.getenv("KAFKA_TOPIC")
    group = os.getenv("KAFKA_GROUP")

    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id=group,
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

    scrapyd_url = os.getenv("SCRAPYD_URL")
    scrapyd_port = os.getenv("SCRAPYD_PORT")
    scrapyd_project = os.getenv("SCRAPYD_PROJECT")

    # Loops forever, consumer is an iterator
    for message in consumer:
        search_term = message.value["search"]
        print(f"Scraping: {search_term}")
        # Share primary key for this search
        search_id = str(uuid.uuid4())

        for spider in spiders:
            print(f"Fetching {spider}...")
            requests.post(
                f"http://{scrapyd_url}:{scrapyd_port}/schedule.json",
                data={
                    "project": scrapyd_project,
                    "spider": spider,
                    "uuid": search_id,
                    "search_term": search_term,
                },
            )

        time.sleep(5)
        print("Waiting for more...")
