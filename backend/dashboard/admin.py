from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import AuditLog, Incident, AlertRule


@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = (
        'timestamp', 'user', 'action_type', 'app_label', 'model_name', 'object_id', 'ip_address'
    )
    list_filter = ('action_type', 'app_label', 'model_name', 'timestamp')
    search_fields = ('user_agent', 'metadata')
    date_hierarchy = 'timestamp'


@admin.register(Incident)
class IncidentAdmin(ModelAdmin):
    list_display = ('title', 'status', 'severity', 'created_by', 'assigned_to', 'updated_at')
    list_filter = ('status', 'severity')
    search_fields = ('title', 'notes')


@admin.register(AlertRule)
class AlertRuleAdmin(ModelAdmin):
    list_display = ('name', 'metric_name', 'operator', 'threshold', 'window_minutes', 'severity', 'active')
    list_filter = ('metric_name', 'severity', 'active')
    search_fields = ('name',)

# Register your models here.
