export-local-vars:
	export TEST_DB_URL=postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable
	export TEST_MIGRATIONS_DIR=file://../infra/dev/do/migrations

up:
	docker compose up --build --force-recreate --detach --wait --wait-timeout 30
	sleep 2

down:
	docker compose down --volumes

test-unit:
	DEBUG=1 poetry run python -m pytest tests/unit

watch-test-unit:
	find src tests -name "*.py" | entr make test-unit

test-integration:
	DEBUG=1 poetry run python -m pytest tests/integration

test-all: test-coverage up migrate test-integration down
	
test-coverage:
	poetry run coverage run -m pytest tests/unit
	poetry run coverage combine
	poetry run coverage report -m

type-check:
	poetry run python -m mypy src tests

watch-type-check:
	find src tests -name "*.py" | entr make type-check

fmt:
	poetry run black --preview src tests
	poetry run flake8 src tests

fmt-check:
	poetry run black --preview --check src tests
	poetry run flake8 src tests

docs-build:
	poetry run mkdocs build

watch-docs-build:
	poetry run mkdocs serve -a localhost:8005

check: fmt-check type-check docs-build

check-all: check test-coverage

watch-server:
	poetry run uvicorn main:app --reload

migrate:
	atlas migrate apply \
<<<<<<< HEAD
		--dir "$(INGREDIENTS_TEST_MIGRATIONS_DIR)" \
		--url "$(INGREDIENTS_TEST_DB_URL)" \
=======
		--dir "$(TEST_MIGRATIONS_DIR)" \
		--url "$(TEST_DB_URL)" \
>>>>>>> 940d6e35ba5afe7ded7709e1cea1448f2490d533
		--revisions-schema public
