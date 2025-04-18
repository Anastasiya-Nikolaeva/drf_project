from django.test import TestCase

from .models import User


class UserModelTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(email="test@example.com", password="testpass")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass"))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_str(self):
        user = User.objects.create_user(email="test@example.com", password="testpass")
        self.assertEqual(str(user), "test@example.com")
