from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='batch-index'),
    path('course-categories/', views.course_categories, name='course-categories'),
]
