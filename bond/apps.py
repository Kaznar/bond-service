from django.apps import AppConfig


class BondsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bond'

    def ready(self):
        import bond.signals  # noqa
