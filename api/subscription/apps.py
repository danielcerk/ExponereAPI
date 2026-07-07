from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.subscription'

    def ready(self):
        
        import api.subscription.signals
