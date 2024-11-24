import os
from pathlib import Path

import environ
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class Command(BaseCommand):
    help = "Ensure a superuser exists using environment variables."

    def handle(self, *args, **kwargs):
        username = env("DJANGO_ADMIN_USERNAME")
        email = env("DJANGO_ADMIN_EMAIL")
        password = env("DJANGO_ADMIN_PASSWORD")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists."))
