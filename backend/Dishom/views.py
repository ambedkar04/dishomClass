from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import sys

@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for monitoring
    Returns 200 OK if the application is running
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'Safal Classes API',
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    })

@require_http_methods(["GET"])
def api_info(request):
    """
    API information endpoint
    """
    return JsonResponse({
        'name': 'Safal Classes API',
        'version': '1.0.0',
        'domain': 'safalclasses.com',
        'endpoints': {
            'accounts': '/api/accounts/',
            'batch': '/api/batch/',
            'study': '/api/study/',
            'admin': '/admin/',
        }
    })
