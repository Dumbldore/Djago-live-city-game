from django.core.management.base import BaseCommand
from city.models import BonusCode


class Command(BaseCommand):
    args = ""
    help = "Populates db with codes"

    def _create_tags(self):
        for code, value in CODES:
            bonus_code = BonusCode(code=code, value=value)
            bonus_code.save()
            print(bonus_code)

    def handle(self, *args, **options):
        self._create_tags()


CODES = [
    ("Blechtrommel", 3400),
    ("Kleinhammer", 3400),
    ("Langfuhr", 3400),
    ("T-34", 3400),
    ("Gralath", 3400),
    ("Medizin", 3400),
    ("nekropolia", 3400),
    ("Stadttheater", 3400),
    ("Ołowianka", 3400),
    ("Muzeum", 3400),
    ("Markthalle", 3400),
    ("Dominikanie", 3400),
    ("Grass", 5000),
    ("Pestalozzi", 7000),
    ("Pniewski ", 10000),
    ("Grazyny", 5000),
    ("Aldony", 7000),
    ("Wallenroda", 10000),
    ("Egon", 5000),
    ("Lukasiewicz", 7000),
    ("Turski", 10000),
    ("ETI", 5000),
    ("Chemia", 7000),
    ("Fizyka", 10000),
    ("Niemcy", 5000),
    ("Finowie", 7000),
    ("Anglicy", 10000),
    ("Brygida", 10000),
    ("Katarzyna", 10000),
    ("Mlyn", 10000),
    ("Zbrojownia", 10000),
    ("Zielona", 10000),
    ("was", 1500),
    ("sagte", 1500),
    ("gibt ", 1500),
    ("alle", 1500),
    ("seit", 1500),
    ("muss", 1500),
    ("doch", 1500),
    ("jetzt", 1500),
    ("drei", 1500),
    ("neue", 1500),
    ("damit", 1500),
    ("bereits", 1500),
    ("damit", 1500),
    ("ab", 1500),
    ("ohne", 1500),
    ("sondern", 1500),
    ("selbst", 1500),
    ("ersten", 1500),
    ("nun", 1500),
    ("etwa", 1500),
    ("heute", 1500),
    ("weil", 1500),
    ("ihm", 1500),
    ("manschen", 1500),
    ("ganz", 1500),
    ("anderen", 1500),
    ("rund", 1500),
    ("ihn", 1500),
    ("ende", 1500),
    ("jedoch", 1500),
    ("Zeit", 1500),
    ("uns", 1500),
    ("stadt", 1500),
    ("geht", 1500),
    ("sehr", 1500),
    ("hier", 1500),
]
