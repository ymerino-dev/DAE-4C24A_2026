"""Create or verify the two local test users."""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


TEST_USERS = (
    {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password_env': 'DJANGO_TEST_USER_PASSWORD',
    },
    {
        'username': 'testadmin',
        'email': 'testadmin@example.com',
        'password_env': 'DJANGO_TEST_ADMIN_PASSWORD',
    },
)


class Command(BaseCommand):
    """Create the configured test users when they do not exist yet."""

    help = 'Create or verify the two local test users.'

    def handle(self, *args, **options):
        user_model = get_user_model()

        for config in TEST_USERS:
            password = os.environ.get(config['password_env'])
            if not password:
                raise CommandError(
                    f"Set {config['password_env']} "
                    'before running this command.',
                )

            user, created = user_model.objects.get_or_create(
                username=config['username'],
                defaults={'email': config['email']},
            )

            if created:
                user.set_password(password)
                user.save(update_fields=['password'])
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.username}'),
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'User already exists: {user.username}',
                    ),
                )
