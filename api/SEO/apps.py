from django.apps import AppConfig


class SeoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.SEO'

    def ready(self):
        
        import api.SEO.signals
