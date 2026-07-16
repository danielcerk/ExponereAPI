from django.apps import AppConfig


class LaunchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.launch'

    def ready(self):
        
        import api.launch.signals
