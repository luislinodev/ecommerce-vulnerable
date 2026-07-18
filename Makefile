.PHONY: help build up down logs shell createsuperuser migrate migrations collectstatic clean

help:
	@echo "Available commands:"
	@echo "  make build              - Build Docker images"
	@echo "  make up                 - Start containers"
	@echo "  make down               - Stop containers"
	@echo "  make logs               - Show container logs"
	@echo "  make logs-web           - Show web container logs"
	@echo "  make shell              - Access Django shell"
	@echo "  make createsuperuser    - Create admin user"
	@echo "  make migrate            - Run database migrations"
	@echo "  make migrations         - Create new migrations"
	@echo "  make collectstatic      - Collect static files"
	@echo "  make dbshell            - Access database shell"
	@echo "  make test               - Run tests"
	@echo "  make clean              - Remove containers and volumes"
	@echo "  make restart            - Restart containers"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

shell:
	docker-compose exec web python manage.py shell

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

migrate:
	docker-compose exec web python manage.py migrate

migrations:
	docker-compose exec web python manage.py makemigrations

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

dbshell:
	docker-compose exec db psql -U ${SQL_USER:-ecommerce_user} -d ${SQL_DATABASE:-ecommerce_db}

test:
	docker-compose exec web python manage.py test

clean:
	docker-compose down -v

restart: down up
	@echo "Containers restarted"

# Dev commands
dev: up
	@echo "Development environment started at http://localhost:8000"

dev-logs: logs-web
