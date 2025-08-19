# knack/management/commands/update_lestypes.py
from django.core.management.base import BaseCommand
from ...utility import get_records, post_api_data

class Command(BaseCommand):
    help = 'Fetches lestype data from Knack API and updates Django models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Updating Lestypes..."))
        lestypes = get_records('Lestypes')
        for lestype in lestypes:
            lesvorm = lestype['field_60']
            lesvorm = lesvorm[0].upper() + lesvorm[1:]
            price_ex = lestype['field_66']
            tax = price_ex * 0.21
            price_inc = price_ex + tax
            data = {'naam': lesvorm, 'soort': lestype['field_61'], 'beschrijving': lestype['field_61'], 
                    'duur': lestype['field_63'], 'aantal': lestype['field_64'], 'prijs_ex': price_ex, 'prijs_inc': price_inc}
            response = post_api_data('knack/lestypes', data)
            if response:
                self.stdout.write(f"Status: {response.status_code}")
                if response.status_code == 201:
                    self.stdout.write(self.style.SUCCESS(f"Successfully created lestype: {lesvorm}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Error: {response.text}"))
            else:
                self.stdout.write(self.style.ERROR("Failed to send request"))
        
        self.stdout.write(self.style.SUCCESS("Lestype update finished successfully!"))