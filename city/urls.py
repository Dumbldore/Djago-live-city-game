from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("building/<int:building_id>/", views.building_detail, name="city-building"),
    path("", views.building_list, name="city-list"),
]
