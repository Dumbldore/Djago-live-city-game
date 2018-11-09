import csv
from django.core.management.base import BaseCommand
from city.models import Building


class Command(BaseCommand):
    args = ""
    help = "Populates db with buildings"

    def _create_small_buildings(self):
        with open("male_budynki.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                bld = Building(
                    name=row["Nazwa"],
                    image=row["link do obrazka"],
                    cost=row["koszt"],
                    generate_points=row["liczba generowanych puktów na minute"],
                    generate_people=row["liczba generowanych ludzi na minute"],
                )
                bld.save()
                print(bld)

    def _create_big_buildings(self):
        with open("duze_budynki.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                bld = Building(
                    name=row["Nazwa"],
                    image=row["link do obrazka"],
                    cost=row["koszt"],
                    generate_points=float(row["liczba generowanych puktów na 10 minut"])
                    / 10,
                    generate_people=float(row["liczba generowanych ludzi na 10 minut"])
                    / 10,
                    max_shares=4,
                )
                bld.save()
                print(bld)

    def handle(self, *args, **options):
        self._create_big_buildings()
        self._create_small_buildings()
