import json
from flask import current_app, g
from kafka import KafkaAdminClient, TopicPartition, KafkaProducer
from kafka.consumer import KafkaConsumer


def get_kafka_producer():
    if "kafka_producer" not in g:
        g.kafka_producer = KafkaProducer(
            bootstrap_servers=current_app.config["KAFKA_BOOTSTRAP_SERVERS"],
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )
    return g.kafka_producer


def get_current_queue_length():
    # We are kind of abusing Kafka, its a message stream, not a queue

    # Get last position
    consumer = KafkaConsumer(bootstrap_servers="172.20.0.3:29092,172.20.0.4:39092")
    partition = TopicPartition("search", 0)
    last_message = consumer.end_offsets([partition]).get(partition, 0)

    # Get current position
    client = KafkaAdminClient(bootstrap_servers="172.20.0.3:29092,172.20.0.4:39092")
    current_message = client.list_consumer_group_offsets(group_id="search-group").get(partition).offset

    return last_message - current_message
