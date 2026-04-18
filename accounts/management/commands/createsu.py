from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='mercykibor').exists():
            User.objects.create_superuser(
                username='mercykibor',
                email='mercy@gmail.com',
                password='Admin1234!'
            )
            self.stdout.write('Superuser created successfully')
        else:
            self.stdout.write('Superuser already exists')