from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
    )
    action_type = models.CharField(
        max_length=20,
        choices=
        (
            ("CREATE", "CREATE"),
            ("UPDATE", "UPDATE"),
            ("DELETE", "DELETE"),
            ("LOGIN", "LOGIN"),
            ("LOGOUT", "LOGOUT"),
            ("PAYMENT", "PAYMENT"),
        ),
    )
    app_label = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=64, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    data_before = models.JSONField(null=True, blank=True)
    data_after = models.JSONField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp", "id"]
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["action_type"]),
            models.Index(fields=["app_label", "model_name"]),
            models.Index(fields=["object_id"]),
        ]


class AlertRule(models.Model):
    name = models.CharField(max_length=200)
    metric_name = models.CharField(max_length=100)
    operator = models.CharField(
        max_length=4,
        choices=(
            ("gt", ">"),
            ("ge", ">="),
            ("lt", "<"),
            ("le", "<="),
            ("eq", "=="),
            ("ne", "!="),
        ),
    )
    threshold = models.FloatField()
    window_minutes = models.PositiveIntegerField(default=5)
    severity = models.CharField(
        max_length=10,
        choices=(
            ("info", "info"),
            ("warning", "warning"),
            ("critical", "critical"),
        ),
        default="warning",
    )
    recipients = models.JSONField(default=dict)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_alert_rules",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "id"]
        indexes = [
            models.Index(fields=["metric_name", "active"]),
            models.Index(fields=["severity"]),
        ]


class Incident(models.Model):
    STATUS_CHOICES = (
        ("open", "open"),
        ("acknowledged", "acknowledged"),
        ("resolved", "resolved"),
    )

    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    severity = models.CharField(
        max_length=10,
        choices=(
            ("info", "info"),
            ("warning", "warning"),
            ("critical", "critical"),
        ),
        default="warning",
    )
    rule = models.ForeignKey(
        AlertRule,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="incidents",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_incidents",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_incidents",
    )
    notes = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "id"]
        indexes = [
            models.Index(fields=["status", "severity"]),
            models.Index(fields=["created_at"]),
        ]

# Create your models here.
