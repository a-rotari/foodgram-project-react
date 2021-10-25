from django.core.management.base import BaseCommand, CommandError

from users_api.models import User
from foodgram_api.models import Favorite, ShoppingCart


class Command(BaseCommand):
    help = 'Creates superuser with default password'

    def handle(self, *arga, **options):
        admin = User.objects.filter(is_staff=True)

        if not admin:
            admin = User.objects.create_superuser(
                'admin', password='admin', email='admin@example.com')
            Favorite.objects.create(user=admin)
            ShoppingCart.objects.create(user=admin)
