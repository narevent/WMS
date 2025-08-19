# knack/management/commands/update_instruments.py
from django.core.management.base import BaseCommand
from ...utility import get_records, post_api_data

class Command(BaseCommand):
    help = 'Fetches instrument data from Knack API and updates Django models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Updating Instruments..."))
        instruments = get_records("Instruments")
        for instrument in instruments:
            instr = instrument['field_35']
            instr = instr[0].upper() + instr[1:]
            data = {'naam': instr}
            response = post_api_data('knack/instrumenten', data)
            if response:
                self.stdout.write(f"Status: {response.status_code}")
                if response.status_code == 201:
                    self.stdout.write(self.style.SUCCESS(f"Successfully created instrument: {instr}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Error: {response.text}"))
            else:
                self.stdout.write(self.style.ERROR("Failed to send request"))
        
        self.stdout.write(self.style.SUCCESS("Instrument update finished successfully!"))