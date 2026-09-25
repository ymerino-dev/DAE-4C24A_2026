from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Idempotent bootstrap of the 'admin' superuser."""

    help = 'Create the admin superuser if it does not exist yet.'

    username = 'admin'
    email = 'admin@cine.com'
    password = 'AdminPassword123!'

    def handle(self, *args, **options):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=self.username)
        except user_model.DoesNotExist:
            self._create(user_model)
            return

        self._report_existing(user)

    def _create(self, user_model):
        user_model.objects.create_superuser(
            username=self.username,
            email=self.email,
            password=self.password,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser "{self.username}" created with '
                f'email "{self.email}".'
            )
        )

    def _report_existing(self, user):
        problems = []
        if not user.is_superuser:
            problems.append('is not a superuser')
        if not user.is_staff:
            problems.append('is not staff')
        if user.email != self.email:
            problems.append(
                f'has email "{user.email}" instead of "{self.email}"'
            )

        if problems:
            message = (
                f'User "{self.username}" already exists but '
                f'{" and ".join(problems)}. No changes were made.'
            )
            self.stdout.write(self.style.WARNING(message))
        else:
            message = (
                f'Superuser "{self.username}" already exists. '
                'No changes were made.'
            )
            self.stdout.write(self.style.SUCCESS(message))
