.PHONY: all help start-web start-consumer init-db

all: help

help:
	@echo "init-kafka: Init the Kafka topics"

init-kafka:
	@docker-compose exec kafka1 \
		kafka-topics \
		--create \
		--topic search \
		--bootstrap-server localhost:9092 \
		--partitions 20 \
		--replication-factor 1
