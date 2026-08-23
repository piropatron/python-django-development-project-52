MANAGE := uv run python manage.py

.PHONY: build
build:
	./build.sh

.PHONY: render-start
render-start: build gunicorn-start

.PHONY: gunicorn-start
gunicorn-start:
	gunicorn task_manager.wsgi

.PHONY: test
test:
	uv run pytest

.PHONY: setup
setup: db-clean install migrate

.PHONY: install
install:
	@uv sync

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: collectstatic
collectstatic:
	@$(MANAGE) collectstatic --noinput

.PHONY: run
run:
	uv run manage.py tailwind runserver

.PHONY: makemigrations
makemigrations:
	@$(MANAGE) makemigrations

.PHONY: makemessages
makemessages:
	@$(MANAGE) makemessages --locale ru_RU

.PHONY: compilemessages
compilemessages:
	@$(MANAGE) compilemessages

.PHONY: lint
lint:
	uv run ruff check task_manager

.PHONY: lint-fix
lint-fix:
	uv run ruff check task_manager --fix


