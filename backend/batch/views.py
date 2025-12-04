from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import CourseCategory


def index(request):
    """Simple placeholder view for the batch app."""
    return JsonResponse({"status": "ok", "app": "batch"})


@require_GET
def course_categories(request):
    """Return list of course categories for frontend consumption."""
    data = list(CourseCategory.objects.values("id", "name", "code"))
    return JsonResponse({"results": data})
