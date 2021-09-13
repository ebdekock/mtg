import json
from flask import current_app, g
from kafka import KafkaProducer


def get_kafka_producer():
    if "kafka_producer" not in g:
        g.kafka_producer = KafkaProducer(
            bootstrap_servers=current_app.config["KAFKA_BOOTSTRAP_SERVERS"],
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )
    return g.kafka_producer
