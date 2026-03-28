install:
	uv sync

build:
	./build.sh

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

render-start:
	gunicorn task_manager.wsgi