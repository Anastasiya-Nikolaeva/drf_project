from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from materials.models import Course, Lesson


class CustomUserManager(BaseUserManager):
    """
    Менеджер для пользовательской модели User.

    Методы:
        create_user: Создает и сохраняет обычного пользователя с указанным email и паролем.
        create_superuser: Создает и сохраняет суперпользователя с указанным email и паролем.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с указанным email и паролем.

        Аргументы:
            email (str): Адрес электронной почты пользователя.
            password (str, optional): Пароль пользователя.
            **extra_fields: Дополнительные поля для пользователя.

        Возвращает:
            User: Созданный пользователь.
        """
        if not email:
            raise ValueError("Поле электронной почты должно быть задано")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.

        Аргументы:
            email (str): Адрес электронной почты суперпользователя.
            password (str, optional): Пароль суперпользователя.
            **extra_fields: Дополнительные поля для суперпользователя.

        Возвращает:
            User: Созданный суперпользователь.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Пользовательская модель пользователя.

    Атрибуты:
        username (str): Имя пользователя (по умолчанию "default_username").
        email (str): Адрес электронной почты пользователя (уникальный).
        phone (str): Номер телефона пользователя (необязательный).
        city (str): Город пользователя (необязательный).
        avatar (ImageField): Фото пользователя (необязательное).
        is_active (bool): Указывает, активен ли пользователь.
    """

    username = models.CharField(max_length=150, default="default_username")
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фотографию",
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Payment(models.Model):
    """
    Модель платежа.

    Атрибуты:
        user (User): Пользователь, который произвел платеж.
        payment_date (DateField): Дата платежа.
        paid_course (Course): Курс, за который был произведен платеж (необязательный).
        paid_lesson (Lesson): Урок, за который был произведен платеж (необязательный).
        amount (DecimalField): Сумма платежа.
        payment_method (str): Метод платежа (наличные или перевод на счет).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="payments", on_delete=models.CASCADE
    )
    payment_date = models.DateField()
    paid_course = models.ForeignKey(
        Course, null=True, blank=True, on_delete=models.CASCADE
    )
    paid_lesson = models.ForeignKey(
        Lesson, null=True, blank=True, on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=10, choices=[("cash", "Наличные"), ("transfer", "Перевод на счет")]
    )

    def __str__(self) -> str:
        """
        Возвращает строковое представление платежа.

        Возвращает:
            str: Строка, содержащая информацию о пользователе, курсе или уроке и дате платежа.
        """
        return f"Платеж от {self.user.email} за {self.paid_course or self.paid_lesson} от {self.payment_date}"
