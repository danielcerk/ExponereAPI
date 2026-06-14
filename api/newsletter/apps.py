from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.newsletter'

    def ready(self):
        
        import api.newsletter.signals
