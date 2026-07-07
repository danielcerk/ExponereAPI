from django.apps import AppConfig


class MarketingConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.marketing'

    def ready(self):
        
        import api.marketing.signals
