#  active_all_users
# python manage.py activate_users

from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Activate users'

    def handle(self, *args, **options):
        # Your logic to activate users
        users_to_activate = CustomUser.objects.filter(is_active=False)  # Example query to get inactive users
        for user in users_to_activate:
            user.is_active = True
            user.save()
        self.stdout.write(self.style.SUCCESS('Users activated successfully'))



