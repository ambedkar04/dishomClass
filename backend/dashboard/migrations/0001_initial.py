from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action_type', models.CharField(choices=[('CREATE', 'CREATE'), ('UPDATE', 'UPDATE'), ('DELETE', 'DELETE'), ('LOGIN', 'LOGIN'), ('LOGOUT', 'LOGOUT'), ('PAYMENT', 'PAYMENT')], max_length=20)),
                ('app_label', models.CharField(max_length=100)),
                ('model_name', models.CharField(max_length=100)),
                ('object_id', models.CharField(blank=True, max_length=64, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=512, null=True)),
                ('data_before', models.JSONField(blank=True, null=True)),
                ('data_after', models.JSONField(blank=True, null=True)),
                ('metadata', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp', 'id'],
            },
        ),
        migrations.CreateModel(
            name='AlertRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('metric_name', models.CharField(max_length=100)),
                ('operator', models.CharField(choices=[('gt', '>'), ('ge', '>='), ('lt', '<'), ('le', '<='), ('eq', '=='), ('ne', '!=')], max_length=4)),
                ('threshold', models.FloatField()),
                ('window_minutes', models.PositiveIntegerField(default=5)),
                ('severity', models.CharField(choices=[('info', 'info'), ('warning', 'warning'), ('critical', 'critical')], default='warning', max_length=10)),
                ('recipients', models.JSONField(default=dict)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_alert_rules', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('open', 'open'), ('acknowledged', 'acknowledged'), ('resolved', 'resolved')], default='open', max_length=20)),
                ('severity', models.CharField(choices=[('info', 'info'), ('warning', 'warning'), ('critical', 'critical')], default='warning', max_length=10)),
                ('notes', models.TextField(blank=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_incidents', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_incidents', to=settings.AUTH_USER_MODEL)),
                ('rule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incidents', to='dashboard.alertrule')),
            ],
            options={
                'ordering': ['-updated_at', 'id'],
            },
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['timestamp'], name='dashboard_auditlog_ts_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['action_type'], name='dashboard_auditlog_action_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['app_label', 'model_name'], name='dashboard_auditlog_model_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['object_id'], name='dashboard_auditlog_object_idx'),
        ),
        migrations.AddIndex(
            model_name='alertrule',
            index=models.Index(fields=['metric_name', 'active'], name='dashboard_alertrule_metric_active_idx'),
        ),
        migrations.AddIndex(
            model_name='alertrule',
            index=models.Index(fields=['severity'], name='dashboard_alertrule_severity_idx'),
        ),
        migrations.AddIndex(
            model_name='incident',
            index=models.Index(fields=['status', 'severity'], name='dashboard_incident_status_severity_idx'),
        ),
        migrations.AddIndex(
            model_name='incident',
            index=models.Index(fields=['created_at'], name='dashboard_incident_created_at_idx'),
        ),
    ]

