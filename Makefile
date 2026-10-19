.PHONY: up down build test

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

test:
	python -m pytest tests -q
