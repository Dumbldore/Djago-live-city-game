from django.contrib import admin
from .models import Patrol2, Building, Share, BonusCode, UsedBonusCode

# Register your models here.

admin.site.register(Patrol2)
admin.site.register(Building)
admin.site.register(Share)
admin.site.register(BonusCode)
admin.site.register(UsedBonusCode)
