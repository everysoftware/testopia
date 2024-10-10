.PHONY: run
run:
	docker-compose up db redis -d --build
	python -m app

.PHONY: generate
generate:
	docker-compose up db redis -d --build
	alembic revision --m="$(NAME)" --autogenerate

.PHONY: upgrade
upgrade:
	docker-compose up db redis -d --build
	alembic upgrade head
