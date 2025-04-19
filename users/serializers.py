from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели платежа.

    Поля:
        user (User): Пользователь, который произвел платеж.
        payment_date (DateField): Дата платежа.
        paid_course (Course): Курс, за который был произведен платеж (необязательный).
        paid_lesson (Lesson): Урок, за который был произведен платеж (необязательный).
        amount (DecimalField): Сумма платежа.
        payment_method (str): Метод платежа (наличные или перевод на счет).
    """

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользовательской модели.

    Поля:
        email (str): Адрес электронной почты пользователя.
        phone (str): Номер телефона пользователя (необязательный).
        city (str): Город пользователя (необязательный).
        avatar (ImageField): Фото пользователя (необязательное).
        payments (PaymentSerializer): Список платежей, связанных с пользователем.
    """

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["email", "phone", "city", "avatar", "payments"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.

    Поля:
        email (str): Адрес электронной почты пользователя.
        password (str): Пароль пользователя (только для записи).
        phone (str): Номер телефона пользователя (необязательный).
        city (str): Город пользователя (необязательный).
        avatar (ImageField): Фото пользователя (необязательное).
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "phone", "city", "avatar"]

    def create(self, validated_data):
        """
        Создает нового пользователя с указанными данными.

        Аргументы:
            validated_data (dict): Данные для создания пользователя.

        Возвращает:
            User: Созданный пользователь.
        """
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
