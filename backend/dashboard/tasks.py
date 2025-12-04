from datetime import timedelta
from django.utils.timezone import now
from celery import shared_task
from django.apps import apps


@shared_task
def aggregate_metrics():
    end = now()
    start = end - timedelta(days=1)
    User = apps.get_model('accounts', 'CustomUser')
    active = 0
    signups = 0
    if User:
        active = User.objects.filter(last_login__gte=start, last_login__lt=end).count()
        signups = User.objects.filter(date_joined__gte=start, date_joined__lt=end).count()
    return {
        'active_users_24h': active,
        'new_signups_24h': signups,
    }

