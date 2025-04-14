from rest_framework import generics, viewsets

from rest_framework import permissions
from users.permissions import IsModerator, IsOwner
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create']:
            # Разрешить создание курсов только авторизованным пользователям
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['destroy']:
            # Разрешить удаление курсов только владельцам
            self.permission_classes = [permissions.IsAuthenticated, IsOwner]
        elif self.action in ['list', 'retrieve', 'update']:
            # Разрешить доступ модераторам и владельцам
            self.permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Привязка создаваемого курса к авторизованному пользователю
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Ограничение списка курсов только для владельца
        if self.request.user.is_authenticated:
            return self.queryset.filter(owner=self.request.user)
        return self.queryset.none()  # Если пользователь не авторизован, возвращаем пустой queryset


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator]


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = []


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator]


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator]


class LessonDeleteView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = []
