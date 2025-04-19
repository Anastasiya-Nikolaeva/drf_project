from django.conf import settings
from django.db import models

from materials.validators import validate_youtube_url


class Course(models.Model):
    """
    Модель курса.

    Атрибуты:
        title (str): Название курса.
        owner (User): Владелец курса (пользователь).
        preview_image (ImageField): Изображение-превью курса.
        description (str): Описание курса.
        price (DecimalField): Цена курса.
    """

    title = models.CharField(max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    preview_image = models.ImageField(
        upload_to="course_previews/", null=True, blank=True
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    def __str__(self) -> str:
        """Возвращает строковое представление курса (название)."""
        return str(self.title)


class Lesson(models.Model):
    """
    Модель урока.

    Атрибуты:
        title (str): Название урока.
        description (str): Описание урока.
        preview_image (ImageField): Изображение-превью урока.
        video_url (str): URL видео на YouTube.
        course (Course): Курс, к которому принадлежит урок.
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(
        upload_to="lesson_previews/", null=True, blank=True
    )
    video_url = models.URLField(
        validators=[validate_youtube_url], null=True, blank=True
    )
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Возвращает строковое представление урока (название)."""
        return str(self.title)


class Subscription(models.Model):
    """
    Модель подписки пользователя на курс.

    Атрибуты:
        user (User): Пользователь, который подписался на курс.
        course (Course): Курс, на который подписан пользователь.

    Метаданные:
        unique_together: Уникальность подписки для пользователя и курса.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "course",
        )  # Уникальность подписки для пользователя и курса

    def __str__(self) -> str:
        """Возвращает строковое представление подписки (пользователь и курс)."""
        return f"{self.user.username} подписался на {self.course.title}"
