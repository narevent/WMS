# knack/management/commands/update_key.py
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key

class Command(BaseCommand):
    help = 'Fetches instrument data from Knack API and updates Django models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Successfully created key: {get_random_secret_key()}"))
