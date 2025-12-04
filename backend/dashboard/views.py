from datetime import datetime, timedelta
from typing import Any, Dict, List

from django.apps import apps
from django.db.models import Count, Sum
from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import AuditLog, Incident, AlertRule
from .serializers import AuditLogSerializer, IncidentSerializer, AlertRuleSerializer
from .permissions import IsSuperAdmin, IsOps, IsSupport


def _parse_range(range_str: str) -> timedelta:
    if not range_str:
        return timedelta(days=7)
    if range_str.endswith("h"):
        return timedelta(hours=int(range_str[:-1]))
    if range_str.endswith("d"):
        return timedelta(days=int(range_str[:-1]))
    return timedelta(days=7)


class MetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rng = request.query_params.get("range", "7d")
        delta = _parse_range(rng)
        end = now()
        start = end - delta
        prev_start = start - delta
        prev_end = start

        data: Dict[str, Dict[str, Any]] = {}

        def period_stats(qs, agg_field=None, sum_field=None):
            if sum_field:
                curr = qs.filter(timestamp__gte=start, timestamp__lt=end).aggregate(total=Sum(sum_field)).get("total") or 0
                prev = qs.filter(timestamp__gte=prev_start, timestamp__lt=prev_end).aggregate(total=Sum(sum_field)).get("total") or 0
            elif agg_field:
                curr = qs.filter(**{f"{agg_field}__gte": start, f"{agg_field}__lt": end}).count()
                prev = qs.filter(**{f"{agg_field}__gte": prev_start, f"{agg_field}__lt": prev_end}).count()
            else:
                curr = qs.filter(created_at__gte=start, created_at__lt=end).count()
                prev = qs.filter(created_at__gte=prev_start, created_at__lt=prev_end).count()
            pct = ((curr - prev) / prev * 100.0) if prev else (100.0 if curr else 0.0)
            return {"current": curr, "prev": prev, "pct": round(pct, 2)}

        User = apps.get_model('accounts', 'CustomUser')
        if User:
            data["active_users"] = period_stats(User.objects.filter(is_active=True), agg_field="last_login")
            data["new_signups"] = period_stats(User.objects.all(), agg_field="date_joined")

        Payment = apps.get_model('payments', 'Payment')
        if Payment:
            data["revenue"] = period_stats(Payment.objects.filter(status='SUCCESS'), sum_field="amount")
            data["failed_payments"] = period_stats(Payment.objects.filter(status='FAILED'), agg_field="timestamp")

        Enrollment = apps.get_model('enrollments', 'Enrollment')
        if Enrollment:
            data["enrollments"] = period_stats(Enrollment.objects.all(), agg_field="created_at")
            data["completions"] = period_stats(Enrollment.objects.filter(status='completed'), agg_field="updated_at")

        LiveView = apps.get_model('live_app', 'LiveViewer')
        if LiveView:
            curr = LiveView.objects.filter(timestamp__gte=start, timestamp__lt=end).aggregate(total=Sum('viewer_count')).get('total') or 0
            prev = LiveView.objects.filter(timestamp__gte=prev_start, timestamp__lt=prev_end).aggregate(total=Sum('viewer_count')).get('total') or 0
            pct = ((curr - prev) / prev * 100.0) if prev else (100.0 if curr else 0.0)
            data["concurrent_live_viewers"] = {"current": curr, "prev": prev, "pct": round(pct, 2)}

        return Response(data)


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsSupport]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        start = params.get('start')
        end = params.get('end')
        user = params.get('user')
        action = params.get('action')
        app_label = params.get('app')
        model_name = params.get('model')
        q = params.get('q')
        if start:
            qs = qs.filter(timestamp__gte=start)
        if end:
            qs = qs.filter(timestamp__lte=end)
        if user:
            qs = qs.filter(user_id=user)
        if action:
            qs = qs.filter(action_type=action)
        if app_label:
            qs = qs.filter(app_label=app_label)
        if model_name:
            qs = qs.filter(model_name=model_name)
        if q:
            qs = qs.filter(models.Q(user_agent__icontains=q) | models.Q(metadata__icontains=q))

        export = params.get('export')
        if export == 'csv':
            return qs
        return qs

    @action(detail=False, methods=['get'])
    def timeline(self, request):
        app_label = request.query_params.get('app')
        model_name = request.query_params.get('model')
        object_id = request.query_params.get('object_id')
        qs = self.get_queryset().filter(app_label=app_label, model_name=model_name, object_id=object_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        export = request.query_params.get('export')
        response = super().list(request, *args, **kwargs)
        if export == 'csv':
            rows: List[Dict[str, Any]] = response.data if isinstance(response.data, list) else response.data.get('results', [])
            header = ['timestamp', 'user', 'action_type', 'app_label', 'model_name', 'object_id', 'ip_address']
            lines = [','.join(header)]
            for r in rows:
                lines.append(','.join([
                    str(r.get('timestamp')), str(r.get('user')), r.get('action_type') or '', r.get('app_label') or '',
                    r.get('model_name') or '', r.get('object_id') or '', r.get('ip_address') or ''
                ]))
            return Response('\n'.join(lines), content_type='text/csv')
        return response


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated, IsOps]

    @action(detail=False, methods=['post'])
    def bulk_resolve(self, request):
        ids = request.data.get('ids', [])
        updated = Incident.objects.filter(id__in=ids).update(status='resolved')
        return Response({'updated': updated})


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.all()
    serializer_class = AlertRuleSerializer
    permission_classes = [IsAuthenticated, IsOps]


class LiveEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        app_filter = request.query_params.get('app')
        qs = AuditLog.objects.filter(action_type__in=["UPDATE", "CREATE", "DELETE"]).order_by('-timestamp')[:100]
        if app_filter:
            qs = qs.filter(app_label=app_filter)
        data = AuditLogSerializer(qs, many=True).data
        return Response({'events': data})


class AdminActionsView(APIView):
    permission_classes = [IsAuthenticated, IsOps]

    def post(self, request):
        action = request.data.get('action')
        if action == 'force_logout':
            ids = request.data.get('user_ids', [])
            try:
                from django.contrib.sessions.models import Session
                from django.contrib.auth import get_user_model
                User = get_user_model()
                sessions = Session.objects.all()
                count = 0
                for session in sessions:
                    data = session.get_decoded()
                    uid = data.get('_auth_user_id')
                    if uid and int(uid) in ids:
                        session.delete()
                        count += 1
                return Response({'sessions_deleted': count})
            except Exception:
                return Response({'error': 'unable to logout users'}, status=status.HTTP_400_BAD_REQUEST)
        if action == 'flag_enrollment':
            Enrollment = apps.get_model('enrollments', 'Enrollment')
            eid = request.data.get('enrollment_id')
            if Enrollment and eid:
                Enrollment.objects.filter(id=eid).update(flagged=True)
                return Response({'flagged': True})
            return Response({'error': 'enrollment not found'}, status=status.HTTP_400_BAD_REQUEST)
        if action == 'resend_invoice':
            Payment = apps.get_model('payments', 'Payment')
            pid = request.data.get('payment_id')
            if Payment and pid:
                return Response({'resent': True})
            return Response({'error': 'payment not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'unknown action'}, status=status.HTTP_400_BAD_REQUEST)
