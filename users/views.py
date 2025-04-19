from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from materials.models import Course, Lesson

from .models import Payment, User
from .serializers import (PaymentSerializer, UserRegisterSerializer,
                          UserSerializer)


class UserRegisterView(generics.CreateAPIView):
    """
    View для регистрации нового пользователя.

    Атрибуты:
        queryset (QuerySet): Все пользователи.
        serializer_class (UserRegisterSerializer): Сериализатор для регистрации пользователя.
        permission_classes (list): Разрешения для доступа (AllowAny).
    """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View для получения и обновления профиля текущего пользователя.

    Атрибуты:
        queryset (QuerySet): Все пользователи.
        serializer_class (UserSerializer): Сериализатор для профиля пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self) -> User:
        """
        Возвращает текущего аутентифицированного пользователя.

        Возвращает:
            User: Текущий пользователь.
        """
        return self.request.user


class PaymentFilter(filters.FilterSet):
    """
    Фильтр для модели платежа.

    Поля:
        paid_course (ModelChoiceFilter): Фильтр по курсу, за который был произведен платеж.
        paid_lesson (ModelChoiceFilter): Фильтр по уроку, за который был произведен платеж.
        payment_method (ChoiceFilter): Фильтр по методу платежа.
    """

    paid_course = filters.ModelChoiceFilter(queryset=Course.objects.all())
    paid_lesson = filters.ModelChoiceFilter(queryset=Lesson.objects.all())
    payment_method = filters.ChoiceFilter(
        choices=[("cash", "Наличные"), ("transfer", "Перевод на счет")]
    )

    class Meta:
        model = Payment
        fields = ["paid_course", "paid_lesson", "payment_method"]


class PaymentListView(generics.ListAPIView):
    """
    View для получения списка платежей.

    Атрибуты:
        queryset (QuerySet): Все платежи.
        serializer_class (PaymentSerializer): Сериализатор для платежей.
        filter_backends (tuple): Фильтры для обработки запросов.
        filterset_class (PaymentFilter): Фильтр для платежей.
        ordering_fields (list): Поля для сортировки.
        ordering (list): Поля по умолчанию для сортировки.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]


class PaymentCreateView(generics.CreateAPIView):
    """
    View для создания нового платежа.

    Атрибуты:
        queryset (QuerySet): Все платежи.
        serializer_class (PaymentSerializer): Сериализатор для платежей.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailView(generics.RetrieveAPIView):
    """
    View для получения деталей платежа.

    Атрибуты:
        queryset (QuerySet): Все платежи.
        serializer_class (PaymentSerializer): Сериализатор для платежей.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDeleteView(generics.DestroyAPIView):
    """
    View для удаления платежа.

    Атрибуты:
        queryset (QuerySet): Все платежи.
        serializer_class (PaymentSerializer): Сериализатор для платежей.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Кастомизированный view для получения токена доступа и обновления.

    Добавляет имя пользователя в ответ.
    """

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для получения токена.

        Аргументы:
            request (Request): Запрос от клиента.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные ключевые аргументы.

        Возвращает:
            Response: Ответ с токеном и именем пользователя.
        """
        response = super().post(request, *args, **kwargs)
        response.data["username"] = request.data.get("username")
        return response
