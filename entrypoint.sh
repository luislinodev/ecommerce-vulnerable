#!/bin/bash

set -e

echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$SQL_PASSWORD psql -h "$SQL_HOST" -U "$SQL_USER" -d "$SQL_DATABASE" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear 2>/dev/null || true

echo "Creating superuser if needed..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created successfully")
else:
    print("Superuser 'admin' already exists")
END

echo "Starting Django application..."
exec "$@"
