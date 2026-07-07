from celery import shared_task

from django.utils import timezone

from .models import CheckoutSessionRecord, Plan


@shared_task()
def disable_canceled_plans():

    now = timezone.now()

    expired_checkouts = CheckoutSessionRecord.objects.filter(
        plan_end_date__lte=now,
        has_access=True
    )

    print(expired_checkouts)

    free_plan = Plan.objects.filter(name='Grátis').first()

    count = 0

    for checkout in expired_checkouts:

        checkout.has_access = False
        checkout.is_completed = False

        checkout.plan = free_plan
        checkout.plan_end_date = None

        checkout.save()

        count += 1

    return f'{count} planos cancelados processados com sucesso'