import os
from pathlib import Path

import environ
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class Command(BaseCommand):
    """
       Custom Django management command to create a superuser.

       Purpose:
       - Ensures that a superuser exists based on environment variables.
       - Useful for automated deployment where admin credentials are predefined.

       Usage:
           python manage.py create_admin

       Environment Variables:
       - `DJANGO_ADMIN_USERNAME`: Username for the superuser.
       - `DJANGO_ADMIN_EMAIL`: Email for the superuser.
       - `DJANGO_ADMIN_PASSWORD`: Password for the superuser.

       Notes:
       - If the superuser already exists, the command does nothing.
    """

    help = "Ensure a superuser exists using environment variables."

    def handle(self, *args, **kwargs):
        """
           Checks for an existing superuser and creates one if absent.
           Outputs success or warning messages based on the operation.
        """
        username = env("DJANGO_ADMIN_USERNAME")
        email = env("DJANGO_ADMIN_EMAIL")
        password = env("DJANGO_ADMIN_PASSWORD")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(self.style.SUCCESS(f"Superuser '{username}' created."))
        else:
            print(self.style.WARNING(f"Superuser '{username}' already exists."))
