from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^addpoints/$', views.addpoints.as_view(), name='addpoints'),
]