from django.apps import AppConfig


class AnalyticConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.analytic'

    def ready(self):
        
        import api.analytic.signals
