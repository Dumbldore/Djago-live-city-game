from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name="blog-home"),
    path("home/", views.home, name="blog-home"),
    path("about/", views.about, name="blog-about"),
    path("kod/", views.kod, name="blog-kod"),
]
