#!/bin/bash

# Init Kafka on startup
python -c 'from web.kafka_lib import init_kafka; init_kafka()'

# Start Flask
flask run --host="$FLASK_HOST" --port="$FLASK_PORT"
