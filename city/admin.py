from django.contrib import admin
from .models import Patrol2 as Patrol, Building, Share, BonusCode, UsedBonusCode

# Register your models here.

@admin.register(UsedBonusCode)
class UsedBonusCodeAdmin(admin.ModelAdmin):
    list_display = ('bonus_code', 'patrol', 'datetime_used')


@admin.register(Patrol)
class PatrolAdmin(admin.ModelAdmin):
    list_display = ("name", "money", "people")


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ("building", "patrol", "date_bought")

# admin.site.register(Share)
admin.site.register(Building)
admin.site.register(BonusCode)

