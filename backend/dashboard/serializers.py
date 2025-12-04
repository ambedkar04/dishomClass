from rest_framework import serializers
from .models import AuditLog, Incident, AlertRule


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = (
            'id', 'timestamp', 'user', 'action_type', 'app_label', 'model_name',
            'object_id', 'ip_address', 'user_agent', 'data_before', 'data_after', 'metadata'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        is_super = bool(user and (user.is_superuser or user.groups.filter(name__in=['SuperAdmin']).exists()))
        if not is_super:
            if 'data_before' in data:
                data['data_before'] = None
            if 'data_after' in data:
                data['data_after'] = None
        return data


class AlertRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRule
        fields = (
            'id', 'name', 'metric_name', 'operator', 'threshold', 'window_minutes',
            'severity', 'recipients', 'active', 'created_by', 'created_at', 'updated_at'
        )


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = (
            'id', 'title', 'status', 'severity', 'rule', 'created_by', 'assigned_to',
            'notes', 'metadata', 'created_at', 'updated_at'
        )
