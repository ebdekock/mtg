import json
import os
from time import sleep
from flask import g
from kafka import KafkaAdminClient, TopicPartition, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable

from kafka.consumer import KafkaConsumer


def init_kafka():
    # Init script to try and create Kafka topic if it doesnt exist
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    topic = os.getenv("KAFKA_TOPIC")
    try:
        client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic_list = NewTopic(name=topic, num_partitions=20, replication_factor=1)
        client.create_topics(new_topics=[topic_list], validate_only=False)
        print(f"Created topic: {topic}")
    except NoBrokersAvailable:
        sleep(30)
        client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic_list = NewTopic(name=topic, num_partitions=20, replication_factor=1)
        client.create_topics(new_topics=[topic_list], validate_only=False)
        print(f"Created topic: {topic}")
    except TopicAlreadyExistsError:
        print(f"Topic already exists: {topic}")
        pass


def get_kafka_producer():
    if "kafka_producer" not in g:
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        g.kafka_producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )
    return g.kafka_producer


def get_current_queue_length():
    # We are kind of abusing Kafka, its a message stream, not a queue. This is also not super
    # responsive and its just used as a rough guideline of how many searches are queued
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    topic = os.getenv("KAFKA_TOPIC")
    group = os.getenv("KAFKA_GROUP")

    # Get last position
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
    partition = TopicPartition(topic, 0)
    last_message = consumer.end_offsets([partition]).get(partition, 0)

    # Get current position
    client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    current_message = client.list_consumer_group_offsets(group_id=group).get(partition).offset

    return last_message - current_message
