from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("", views.building_list, name="city-home"),
    path("city/", views.building_list, name="city-home"),
    path("kod/", views.kod, name="city-code"),
    path("building/<int:building_id>/", views.building_detail, name="city-building"),
    path("patrol/<int:patrol_id>/", views.patrol_detail, name="city-patrol"),
    path("stats/", views.stats, name="city-stats"),
]
