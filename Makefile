install:
	uv sync

# Сборка статики
collectstatic:
	uv run python manage.py collectstatic --no-input

# Применение миграций
migrate:
	uv run python manage.py migrate

# Команда сборки для Render (согласно заданию)
build:
	./build.sh

# Команда запуска (согласно заданию, с учетом uv)
render-start:
	uv run gunicorn task_manager.wsgi