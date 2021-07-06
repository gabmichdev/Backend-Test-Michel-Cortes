from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token")


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUsersAPITests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "username": "testuser",
            "password": "test123.@1",
            "name": "test",
        }

    # USERS
    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        create_user(**self.payload)

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        self.payload["password"] = "pw"

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = (
            get_user_model().objects.filter(username=self.payload["username"]).exists()
        )
        self.assertFalse(user_exists)

    # TOKEN
    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        create_user(**self.payload)
        payload = {"username": "testuser", "password": "test123.@1"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(**self.payload)
        payload = {"username": "testuser", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is  not created if user does not exist"""
        payload = {"username": "testuser", "password": "test123.@1"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that username and password are required"""
        payload = {"username": "testuser", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)