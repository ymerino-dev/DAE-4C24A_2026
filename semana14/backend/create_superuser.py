"""Create the default superuser when it does not exist yet."""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django  # noqa: E402

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402


USERNAME = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
EMAIL = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com')
PASSWORD = os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin123')


def create_superuser():
    """Create the configured superuser only once."""
    user_model = get_user_model()

    if user_model.objects.filter(username=USERNAME).exists():
        print(f'Superuser already exists: {USERNAME}')
        return

    user_model.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD,
    )
    print(f'Superuser created: {USERNAME}')


if __name__ == '__main__':
    create_superuser()
