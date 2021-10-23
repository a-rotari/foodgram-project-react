from django.core.management.base import BaseCommand, CommandError

from users_api.models import User


class Command(BaseCommand):
    help = 'Creates superuser with default password'

    def handle(self, *arga, **options):
        admin = User.objects.filter(is_staff=True)

        if not admin:
            User.objects.create_superuser(
                'admin', password='admin', email='admin@example.com')
