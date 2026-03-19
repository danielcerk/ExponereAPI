from django.apps import AppConfig


class AffiliateConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.affiliate'

    def ready(self):
        
        import api.affiliate.signals
