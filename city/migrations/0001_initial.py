# Generated by Django 2.1.3 on 2018-11-09 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="BonusCode",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=50, verbose_name="Kod do wpisania"),
                ),
                (
                    "value",
                    models.IntegerField(
                        default=100, verbose_name="Guldeny przyznawane za kod"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Building",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, verbose_name="Nazwa budynku"),
                ),
                ("image", models.URLField(blank=True, null=True)),
                (
                    "cost",
                    models.PositiveIntegerField(
                        default=100, verbose_name="Koszt budowy budynku w guldenach"
                    ),
                ),
                (
                    "generate_people",
                    models.PositiveIntegerField(
                        default=1, verbose_name="Przychód guldenów"
                    ),
                ),
                (
                    "generate_points",
                    models.PositiveIntegerField(
                        default=1, verbose_name="Wzrost ludności"
                    ),
                ),
                (
                    "max_shares",
                    models.PositiveIntegerField(
                        default=1,
                        verbose_name="Maksymalna liczba patroli mogąca zbudować budynek",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Patrol2",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="Nazwa patrolu"),
                ),
                (
                    "image",
                    models.ImageField(default="default.jpg", upload_to="profile_pics"),
                ),
                (
                    "money",
                    models.PositiveIntegerField(default=0, verbose_name="Guldeny"),
                ),
                (
                    "people",
                    models.PositiveIntegerField(default=0, verbose_name="Ludność"),
                ),
                ("number_of_built_buildings", models.PositiveIntegerField(default=0)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                )
            ],
        ),
        migrations.CreateModel(
            name="Share",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_bought",
                    models.DateTimeField(auto_now_add=True, verbose_name="Data zakupu"),
                ),
                (
                    "building",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="city.Building",
                        verbose_name="Budynek",
                    ),
                ),
                (
                    "patrol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="city.Patrol2",
                        verbose_name="Patrol",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UsedBonusCode",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "datetime_used",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Czas wykorzystania kodu"
                    ),
                ),
                (
                    "bonus_code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="city.BonusCode",
                        verbose_name="Wykorzystany Kod",
                    ),
                ),
                (
                    "patrol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="city.Patrol2",
                        verbose_name="Patrol",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="building",
            name="shareholders",
            field=models.ManyToManyField(
                blank=True,
                through="city.Share",
                to="city.Patrol2",
                verbose_name="Patrole które zbudowały budynek",
            ),
        ),
    ]