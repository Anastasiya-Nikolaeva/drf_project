from django.urls import path

from .views import (PaymentCreateView, PaymentDeleteView, PaymentDetailView,
                    PaymentListView, UserProfileView)

app_name = "users"

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/create/", PaymentCreateView.as_view(), name="payment-create"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("payments/<int:pk>/delete/", PaymentDeleteView.as_view(), name="payment-delete"),
]
