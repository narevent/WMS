# agenda/management/commands/create_vakanties.py
import datetime
import requests
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from agenda.models import Vakantie

API_URL = "https://opendata.rijksoverheid.nl/v1/infotypes/schoolholidays?output=json"
REGIONS_INCLUDE = {"noord", "heel nederland"}

def current_schoolyear_dates(today=None):
    """Schoolyear runs Aug 1 -> Jul 31. Returns (start_date, end_date)."""
    if today is None:
        today = datetime.date.today()
    if today.month >= 8:  # Aug–Dec
        return datetime.date(today.year, 8, 1), datetime.date(today.year + 1, 7, 31)
    else:  # Jan–Jul
        return datetime.date(today.year - 1, 8, 1), datetime.date(today.year, 7, 31)

def normalize_type(raw: str) -> str:
    t = " ".join((raw or "").split()).lower()
    mapping = {
        "herfstvakantie": "Herfstvakantie",
        "kerstvakantie": "Kerstvakantie",
        "voorjaarsvakantie": "Voorjaarsvakantie",
        "meivakantie": "Meivakantie",
        "zomervakantie": "Zomervakantie",
    }
    return mapping.get(t, (raw or "").strip().capitalize())

class Command(BaseCommand):
    help = "Import Noord (and national) school holidays for the current schoolyear (Aug→Jul)"

    def handle(self, *args, **kwargs):
        school_start, school_end = current_schoolyear_dates()
        self.stdout.write(f"Importing holidays with start in [{school_start} .. {school_end}] for Noord…")

        resp = requests.get(API_URL, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        items = {}
        for entry in data:
            for content in entry.get("content", []):
                for vac in content.get("vacations", []):
                    naam = normalize_type(vac.get("type", ""))
                    for region in vac.get("regions", []):
                        region_name = (region.get("region") or "").strip().lower()
                        if region_name not in REGIONS_INCLUDE:
                            continue

                        start_dt = parse_datetime(region.get("startdate"))
                        end_dt = parse_datetime(region.get("enddate"))
                        if not start_dt or not end_dt:
                            continue
                        start, eind = start_dt.date(), end_dt.date()

                        if school_start <= start <= school_end:
                            items[(naam, start)] = (naam, start, eind)

        created, updated = 0, 0
        for _, (naam, start, eind) in sorted(items.items(), key=lambda kv: kv[1][1]):
            print(naam, start, eind)
            obj, was_created = Vakantie.objects.update_or_create(
                naam=naam,
                start=start,
                defaults={"eind": eind},
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created {naam}: {start} – {eind}"))
            else:
                updated += 1
                self.stdout.write(self.style.WARNING(f"Updated {naam}: {start} – {eind}"))

        self.stdout.write(self.style.SUCCESS(f"Done. Created {created}, updated {updated}."))
