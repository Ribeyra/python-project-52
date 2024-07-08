start:
	poetry run python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

dev-start:
	poetry run python manage.py runserver

build:
	./build.sh

dev-build:
	poetry install
	poetry run python manage.py migrate

shell:
	poetry run python manage.py shell_plus --ipython

test:
	poetry run python manage.py test
