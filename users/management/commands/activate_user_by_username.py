# activate_user_by_username
# python manage.py activate_user_by_username mostafa

from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Activate a user by username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user to activate')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        User = CustomUser
        try:
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully activated user with username {username}'))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'User with username {username} does not exist'))
