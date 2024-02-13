from django.apps import AppConfig


class MyinvestmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myinvestment'

    def ready(self):
        import myinvestment.signals
