MANAGE := uv run python manage.py

.PHONY: build
build:
	./build.sh

.PHONY: render-start
render-start:
	gunicorn task_manager.wsgi
	
.PHONY: test
test:
	uv run pytest

.PHONY: setup
setup: db-clean install migrate

.PHONY: install
install:
	@uv sync

.PHONY: db-clean
db-clean:
	@rm db.sqlite3 || true

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: run
run:
	uv run manage.py runserver

.PHONY: lint
lint:
	uv run ruff check task_manager

