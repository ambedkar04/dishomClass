from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from dashboard.models import AuditLog


class Command(BaseCommand):
    help = 'Archive audit logs older than 365 days'

    def handle(self, *args, **options):
        cutoff = now() - timedelta(days=365)
        qs = AuditLog.objects.filter(timestamp__lt=cutoff)
        count = qs.count()
        qs.delete()
        self.stdout.write(self.style.SUCCESS(f'Archived {count} audit logs'))

