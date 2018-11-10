from django.apps import AppConfig


class CityConfig(AppConfig):
    name = "city"

    def ready(self):
        import city.signals
