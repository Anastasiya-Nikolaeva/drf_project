from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели урока.

    Поля:
        video_url (str): URL видео на YouTube с валидацией.
    """

    video_url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели курса.

    Поля:
        lessons (LessonSerializer): Список уроков, связанных с курсом.
        lesson_count (int): Количество уроков в курсе.
        is_subscribed (bool): Указывает, подписан ли текущий пользователь на курс.
    """

    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, obj: Course) -> int:
        """
        Возвращает количество уроков в курсе.

        Аргументы:
            obj (Course): Экземпляр курса.

        Возвращает:
            int: Количество уроков.
        """
        return obj.lessons.count()

    def get_is_subscribed(self, obj: Course) -> bool:
        """
        Проверяет, подписан ли текущий пользователь на курс.

        Аргументы:
            obj (Course): Экземпляр курса.

        Возвращает:
            bool: True, если пользователь подписан, иначе False.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False
