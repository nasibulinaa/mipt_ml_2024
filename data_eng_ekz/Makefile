.PHONY: up down unpause reload bash python clean

all: up

user_id = $(shell id -u)

docker-compose.yaml:
	@echo "Downloaing compose file..."
	curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.2/docker-compose.yaml'

airflow.sh:
	@echo "Downloading airflow.sh..."
	curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.2/airflow.sh'
	chmod +x airflow.sh

.env:
	@echo "Creating directories..."
	-mkdir -p ./logs ./plugins ./config
	@echo "User ID is $(user_id). Writing it to env file..."
	echo "AIRFLOW_UID=$(user_id)" > .env

done_cfg.flag: docker-compose.yaml .env
	@echo "Creating default airflow config..."
	docker compose run airflow-cli airflow config list
	@echo "Running custom cfg..."
	./user_cfg.sh
	@echo "Triggering ariflow init..."
	docker compose up airflow-init
	@touch done_cfg.flag

up: done_cfg.flag
	@echo "-- Doing docker compose up -d..."
	docker compose up -d
	@echo "Unpausing DAG..."
	@make unpause

down:
	@echo "-- Doing docker compose down..."
	-docker compose down

unpause: done_cfg.flag
	docker compose exec airflow-apiserver airflow dags unpause pipeline_dag

reload: done_cfg.flag
	docker compose exec airflow-apiserver airflow dags reserialize

bash: airflow.sh done_cfg.flag
	./airflow.sh bash

python: airflow.sh done_cfg.flag
	./airflow.sh python

clean: down
	@echo "-- Cleaning up..."
	-docker compose down --volumes --remove-orphans
	rm -rf ./logs \
		./plugins \
		./config \
		./data \
		./results \
		.env \
		done_cfg.flag \
		docker-compose.yaml \
		airflow.sh
