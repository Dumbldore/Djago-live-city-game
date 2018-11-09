from django.db import models
from django.contrib.auth.models import User


class Rule(models.Model):
    name = models.CharField


class Patrol2(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Nazwa patrolu", max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    money = models.PositiveIntegerField("Guldeny", default=0)
    people = models.PositiveIntegerField("Ludność", default=0)
    number_of_built_buildings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Profile {self.id}"


class Building(models.Model):
    """"""

    name = models.CharField("Nazwa budynku", max_length=128)
    shareholders = models.ManyToManyField(
        Patrol2,
        through="Share",
        verbose_name="Patrole które zbudowały budynek",
        blank=True,
    )
    image = models.URLField(blank=True, null=True)

    cost = models.PositiveIntegerField("Koszt budowy budynku w guldenach", default=100)
    generate_people = models.PositiveIntegerField("Przychód guldenów", default=1)
    generate_points = models.PositiveIntegerField("Wzrost ludności", default=1)

    max_shares = models.PositiveIntegerField(
        "Maksymalna liczba patroli mogąca zbudować budynek", default=1
    )

    def __str__(self):
        return self.name


class Share(models.Model):
    patrol = models.ForeignKey(Patrol2, on_delete=models.CASCADE, verbose_name="Patrol")
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, verbose_name="Budynek"
    )
    date_bought = models.DateTimeField("Data zakupu", auto_now_add=True)

    def __str__(self):
        return f"jeden udział {self.patrol} w {self.building}, {self.date_bought}"


class BonusCode(models.Model):
    code = models.CharField("Kod do wpisania", max_length=50)
    value = models.IntegerField("Guldeny przyznawane za kod", default=100)

    def __str__(self):
        return f'"{self.code}": {self.value} guldenów'


class UsedBonusCode(models.Model):
    patrol = models.ForeignKey(Patrol2, on_delete=models.CASCADE, verbose_name="Patrol")
    bonus_code = models.ForeignKey(
        BonusCode, on_delete=models.CASCADE, verbose_name="Wykorzystany Kod"
    )
    datetime_used = models.DateTimeField("Czas wykorzystania kodu", auto_now_add=True)

    def __str__(self):
        return f'"{self.bonus_code.code}": wykorzystany przez {self.patrol.name} o {self.datetime_used}'
