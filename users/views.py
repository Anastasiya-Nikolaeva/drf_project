from django_filters import rest_framework as filters
from rest_framework import generics

from materials.models import Course, Lesson

from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PaymentFilter(filters.FilterSet):
    payment_date = filters.DateFilter(field_name="payment_date", lookup_expr="exact")
    paid_course = filters.ModelChoiceFilter(queryset=Course.objects.all())
    paid_lesson = filters.ModelChoiceFilter(queryset=Lesson.objects.all())
    payment_method = filters.ChoiceFilter(
        choices=[("cash", "Наличные"), ("transfer", "Перевод на счет")]
    )

    class Meta:
        model = Payment
        fields = ["payment_date", "paid_course", "paid_lesson", "payment_method"]


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDeleteView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
