APP_PATH = app
TESTS_PATH = tests

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

.PHONY: format
format:
	ruff format $(APP_PATH) $(TESTS_PATH)

.PHONY: lint
lint:
	ruff check $(APP_PATH) $(TESTS_PATH) --fix
	mypy $(APP_PATH) --install-types --enable-incomplete-feature=NewGenericSyntax

.PHONY: freeze
freeze:
	pip freeze > requirements.txt
