# active_user_by_id

from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Create activation link for a specific user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID of the user to activate')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        User = CustomUser
        try:
            user = User.objects.get(pk=user_id)
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully activated user with ID {user_id}'))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'User with ID {user_id} does not exist'))