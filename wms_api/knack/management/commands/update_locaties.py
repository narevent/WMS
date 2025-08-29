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
            kaart = locatie['field_42']['url']
            data = {'naam': naam, 'adres': adres, 'kaart': kaart}
            response = get_or_create_api_data('knack/locaties', data)
            if response:
                self.stdout.write(f"Status: {response.status_code}")
                if response.status_code == 201:
                    self.stdout.write(self.style.SUCCESS(f"Successfully created locatie: {locatie}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Error: {response.text}"))
            else:
                self.stdout.write(self.style.ERROR("Failed to send request"))
        
        self.stdout.write(self.style.SUCCESS("Locaties update finished successfully!"))