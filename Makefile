.PHONY: all help start-web start-consumer init-db

all: help

help:
	@echo "start-web: Start front end\nstart-consumer: Start Kafka consumer\ninit-db: Init the database\ninit-kafka: Init the Kafka topics"

start-web: export FLASK_APP = web
start-web: export FLASK_ENV = development
start-web:
	@flask run --port=5000

start-consumer:
	@(cd scraper && python consumer.py)

init-db: export FLASK_APP = web
init-db: export FLASK_ENV = development
init-db:
	@flask init-db

init-kafka:
	@docker-compose exec kafka-1 \
		kafka-topics \
		--create \
		--topic search \
		--bootstrap-server localhost:9092 \
		--partitions 20 \
		--replication-factor 1
