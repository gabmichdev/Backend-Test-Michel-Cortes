from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_successful(self):
        """Test creating a new user with username is successful"""
        username = "testuser1"
        password = "test123"
        user = get_user_model().objects.create_user(
            username=username, password=password
        )
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_new_super_user(self):
        """Test creating a new super user"""
        username = "testuser2"
        password = "test123"
        user = get_user_model().objects.create_superuser(
            username=username, password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
