from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonAndSubscriptionTests(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.owner = User.objects.create_user(
            email="owner@example.com", password="testpass"
        )
        self.moderator = User.objects.create_user(
            email="moderator@example.com", password="testpass", is_staff=True
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="testpass"
        )

        # Создаем курс и урок
        self.course = Course.objects.create(title="Test Course", owner=self.owner)
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course)

    def test_create_lesson_as_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            "/materials/lessons/create/",
            {
                "title": "Новый урок",
                "description": "Это описание тестового урока.",
                "course": self.course.id,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Пример валидного URL
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_as_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(
            "/materials/lessons/create/",
            {
                "title": "Новый урок",
                "description": "Это описание тестового урока.",
                "course": self.course.id,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_as_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(
            "/materials/lessons/create/",
            {
                "title": "Новый урок",
                "description": "Это описание тестового урока.",
                "course": self.course.id,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(
            "/materials/subscribe/", {"course_id": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.other_user, course=self.course)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(
            "/materials/subscribe/", {"course_id": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscribe_to_nonexistent_course(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post("/materials/subscribe/", {"course_id": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_subscription_not_found(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete("/materials/subscribe/", {"course_id": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_lesson_without_authentication(self):
        response = self.client.post(
            "/materials/lessons/create/",
            {"title": "New Lesson", "course": self.course.id},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
