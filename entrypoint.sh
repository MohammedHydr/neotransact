#!/bin/sh

set -e

echo "Applying database migrations..."
poetry run python manage.py migrate

# static file in production not used
if [ "$ENVIRONMENT" = "production" ]; then
    echo "Collecting static files..."
    poetry run python manage.py collectstatic --no-input
fi

# create a django superuser in the dockerrrr
echo "Checking for Django superuser creation..."
poetry run python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv('DJANGO_ADMIN_USERNAME')
email = os.getenv('DJANGO_ADMIN_EMAIL')
password = os.getenv('DJANGO_ADMIN_PASSWORD')

if username and email and password:
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser {username}...")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print(f"Superuser {username} already exists.")
else:
    print("Django superuser credentials not provided in environment variables. Skipping superuser creation.")
EOF

# switch between production and development for a real scenario
if [ "$ENVIRONMENT" = "production" ]; then
    echo "Running in production mode"
    exec poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
elif [ "$ENVIRONMENT" = "development" ]; then
    echo "Running in development mode"
    exec poetry run python manage.py runserver 0.0.0.0:8000
else
    echo "ENVIRONMENT variable is not set. Exiting."
    exit 1
fi
