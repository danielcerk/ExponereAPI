from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.feedback'

    def ready(self):
        
        import api.feedback.signals
