from django.apps import AppConfig


class PluginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.plugin'

    def ready(self):
        
        import api.plugin.signals
