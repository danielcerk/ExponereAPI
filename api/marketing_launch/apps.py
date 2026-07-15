from django.apps import AppConfig


class MarketingLaunchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.marketing_launch'

    def ready(self):
        
        import api.marketing_launch.signals
