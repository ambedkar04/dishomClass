# Dashboard App

## Install

- Add `dashboard` to `INSTALLED_APPS` in `Dishom/settings.py`.
- Install optional deps: `channels`, `channels_redis`, `celery`, `django-redis`.
- Configure env vars: `REDIS_URL`, `CELERY_BROKER`, `ALERT_EMAILS`.
- Run: `python manage.py makemigrations dashboard && python manage.py migrate`.

## API

- `GET /api/dashboard/metrics/?range=7d`
- `GET /api/dashboard/logs/?app=live_app&action=UPDATE&page=1`
- `POST /api/dashboard/alerts/` body: `{ name, metric_name, operator, threshold, window_minutes }`
- `GET /api/dashboard/incidents/?status=open`
- `GET /api/dashboard/live-events/`
- `POST /api/dashboard/actions/` `{ action: 'force_logout', user_ids: [1,2] }`

## WebSocket

- `ws://<host>/ws/dashboard/live-events/<app>/`
- Message: `{ type: 'event', app: 'live_class', kind: 'start|stop|viewer_count', payload: {...}, ts: '<iso>' }`

## Celery

- Task `dashboard.tasks.aggregate_metrics`
- Beat: every 5 minutes

## Indexes

- `AuditLog(timestamp)`, `(action_type)`, `(app_label, model_name)`, `(object_id)`
- `AlertRule(metric_name, active)`
- `Incident(status, severity)`, `(created_at)`

## Retention

- `python manage.py archive_audit_logs`
