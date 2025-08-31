# knack/management/commands/update_locaties.py
from django.core.management.base import BaseCommand
from ...utility import get_records, post_api_data, get_or_create_api_data

class Command(BaseCommand):
    help = 'Fetches location data from Knack API and updates Django models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Updating Locaties..."))
        locaties = get_records('Zalen')
        for locatie in locaties:
            naam = locatie['field_37']
            adres = locatie['field_40']
            url = locatie['field_42']['url']
            kaart = url if url else ''
            data = {'naam': naam, 'adres': adres, 'kaart': kaart}
            print(data)
            response, created = get_or_create_api_data('knack/locaties', data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created locatie: {naam}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Successfully fetched locatie: {naam}"))
        
        self.stdout.write(self.style.SUCCESS("Locaties update finished"))