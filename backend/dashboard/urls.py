from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MetricsView, AuditLogViewSet, IncidentViewSet, AlertRuleViewSet, LiveEventsView, AdminActionsView

router = DefaultRouter()
router.register(r'logs', AuditLogViewSet, basename='dashboard-logs')
router.register(r'incidents', IncidentViewSet, basename='dashboard-incidents')
router.register(r'alerts', AlertRuleViewSet, basename='dashboard-alerts')

urlpatterns = [
    path('metrics/', MetricsView.as_view(), name='dashboard-metrics'),
    path('live-events/', LiveEventsView.as_view(), name='dashboard-live-events'),
    path('actions/', AdminActionsView.as_view(), name='dashboard-actions'),
    path('', include(router.urls)),
]
