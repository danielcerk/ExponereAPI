from django.apps import AppConfig


class ShippingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.shipping'

    def ready(self):
        
        import api.shipping.signals
