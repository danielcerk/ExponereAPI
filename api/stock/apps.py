from django.apps import AppConfig


class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.stock'

    def ready(self):
        
        import api.stock.signals
