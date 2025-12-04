
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import health_check, api_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/batch/', include('batch.urls')),
    path('api/dashboard/', include('dashboard.urls')),

    path("__reload__/", include("django_browser_reload.urls")),
    
    # Health check & API info
    path('health/', health_check, name='health_check'),
    path('api/', api_info, name='api_info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
