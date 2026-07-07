from django.apps import AppConfig


class CouponConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.coupon'

    def ready(self):

        import api.coupon.signals
