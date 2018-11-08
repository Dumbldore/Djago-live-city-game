from django.contrib import admin
from .models import Patrol
from .models import Building
from .models import Big_Building

admin.site.register(Patrol)
admin.site.register(Building)
admin.site.register(Big_Building)
