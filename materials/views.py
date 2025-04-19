from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .paginators import CustomPageNumberPagination
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == "destroy":
            self.permission_classes = [permissions.IsAuthenticated, IsOwner]
        elif self.action in ["list", "retrieve", "update"]:
            self.permission_classes = [IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(owner=self.request.user)
        return self.queryset.none()


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPageNumberPagination


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.request.data.get("course")
        course = Course.objects.get(id=course_id)

        # Проверка, является ли пользователь владельцем курса
        if course.owner != self.request.user:
            raise PermissionDenied("У вас нет прав на создание урока для этого курса.")

        serializer.save()


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_update(self, serializer):
        lesson = self.get_object()
        if lesson.course.owner != self.request.user:
            raise PermissionDenied("У вас нет прав на редактирование этого урока.")
        serializer.save()


class LessonDeleteView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_destroy(self, instance):
        if instance.course.owner != self.request.user:
            raise PermissionDenied("У вас нет прав на редактирование этого урока.")
        instance.delete()


class SubscriptionView(APIView):
    def get_course(self, request):
        course_id = request.data.get("course_id") or request.query_params.get(
            "course_id"
        )
        if not course_id:
            return None, Response(
                {"error": "Требуется указать course_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return get_object_or_404(Course, id=course_id), None

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"error": "Требуется аутентификация"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        course_item, error_response = self.get_course(request)
        if error_response:
            return error_response

        # Проверяем, существует ли подписка
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Удаляем подписку
            subs_item.delete()
            return Response(
                {"message": "Подписка на курс '{}' удалена.".format(course_item.title)},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            # Создаем новую подписку
            Subscription.objects.create(user=user, course=course_item)
            return Response(
                {
                    "message": "Подписка на курс '{}' добавлена.".format(
                        course_item.title
                    )
                },
                status=status.HTTP_201_CREATED,
            )

    def delete(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"error": "Требуется аутентификация"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        course_item, error_response = self.get_course(request)
        if error_response:
            return error_response

        # Проверяем, существует ли подписка
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Удаляем подписку
            subs_item.delete()
            return Response(
                {"message": "Подписка на курс '{}' удалена.".format(course_item.title)},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "Подписка не найдена."}, status=status.HTTP_404_NOT_FOUND
            )
