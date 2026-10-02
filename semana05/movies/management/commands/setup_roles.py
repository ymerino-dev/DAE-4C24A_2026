from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    """Create 'editores' group with restricted Movie permissions and a test user."""

    help = 'Create editores group with add/change/view Movie permissions and editor_user'

    def handle(self, *args, **options):
        self._create_group_and_permissions()
        self._create_user()

    def _create_group_and_permissions(self):
        group, created = Group.objects.get_or_create(name='editores')

        if created:
            self.stdout.write(
                self.style.SUCCESS('Group "editores" created.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Group "editores" already exists.')
            )

        content_type = ContentType.objects.get_for_model(Movie)
        perms = Permission.objects.filter(
            content_type=content_type,
            codename__in=['add_movie', 'change_movie', 'view_movie']
        )

        group.permissions.set(perms)

        self.stdout.write(
            self.style.SUCCESS(
                f'Assigned {perms.count()} permissions to "editores": '
                f'{", ".join(p.codename for p in perms)}'
            )
        )

    def _create_user(self):
        user_model = get_user_model()
        username = 'editor_user'
        password = 'Editor12345!'

        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={'email': 'editor@cine.com'}
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'User "{username}" created.')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )

        group = Group.objects.get(name='editores')
        user.groups.add(group)
        self.stdout.write(
            self.style.SUCCESS(f'User "{username}" added to "editores" group.')
        )