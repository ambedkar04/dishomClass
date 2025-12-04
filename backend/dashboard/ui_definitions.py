OVERVIEW_PAGE = {
    "layout": {
        "grid": "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4",
    },
    "cards": [
        {"title": "Active Users", "metric_key": "active_users", "spark_range": "7d"},
        {"title": "New Signups", "metric_key": "new_signups", "spark_range": "7d"},
        {"title": "Revenue", "metric_key": "revenue", "spark_range": "7d"},
        {"title": "Failed Payments", "metric_key": "failed_payments", "spark_range": "7d"},
    ],
    "chart": {"type": "timeseries", "range_selector": ["24h", "7d", "30d", "custom"]},
    "feed": {"title": "Activity", "source": "/api/dashboard/logs/"},
}

LOG_EXPLORER = {
    "filters": ["date", "user", "action_type", "app_label", "model_name", "search"],
    "table": {"columns": ["timestamp", "user", "action_type", "app_label", "model_name", "object_id"]},
    "export": {"modes": ["csv", "json"]},
}

INCIDENT_MANAGER = {
    "list": {"columns": ["title", "status", "severity", "assigned_to", "updated_at"]},
    "actions": ["bulk_resolve"],
    "detail": {"timeline": "/api/dashboard/logs/timeline/"},
}

LIVE_FEED = {
    "ws": "ws://localhost:8000/ws/dashboard/live-events/all/",
    "controls": {"pause": True, "filter": ["live_class", "chat", "system"]},
}

MODEL_DRILLDOWN = {
    "timeline_endpoint": "/api/dashboard/logs/timeline/",
}

