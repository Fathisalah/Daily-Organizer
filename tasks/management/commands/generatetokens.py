from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Generate authentication tokens for all existing users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(f'Token created for user: {user.username}')
            else:
                self.stdout.write(f'Token already exists for user: {user.username}')
        self.stdout.write('All tokens processed.')
