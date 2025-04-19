from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CourseViewSet, LessonCreateView, LessonDeleteView,
                    LessonDetailView, LessonListView, LessonUpdateView,
                    SubscriptionView)

app_name = "materials"

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListView.as_view(), name="lesson-list"),
    path("lessons/create/", LessonCreateView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/", LessonDetailView.as_view(), name="lesson-detail"),
    path("lessons/<int:pk>/update/", LessonUpdateView.as_view(), name="lesson-update"),
    path("lessons/<int:pk>/delete/", LessonDeleteView.as_view(), name="lesson-delete"),
    path("subscribe/", SubscriptionView.as_view(), name="subscribe"),
]
