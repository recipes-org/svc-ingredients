up:
	docker compose up --build --force-recreate --detach --wait --wait-timeout 30

down:
	docker compose down

test-unit:
	poetry run python -m pytest tests/unit

watch-test-unit:
	find src tests -name "*.py" | entr make test-unit

test-integration:
	poetry run python -m pytest tests/integration

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
		--dir "$(RECIPES_TEST_MIGRATIONS_DIR)" \
		--url "$(RECIPES_TEST_DB_URL)" \
		--revisions-schema public
