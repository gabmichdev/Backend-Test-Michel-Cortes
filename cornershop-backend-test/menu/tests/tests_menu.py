from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from dateutil import parser

from core.models import Menu
from menu.serializers import MenuDetailSerializer, MenuSerializer, get_meal_time

MENU_URL = reverse("menu:menu-list")


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


def create_staff_user(**kwargs):
    return get_user_model().objects.create_superuser(**kwargs)


def detail_url(menu_id):
    """Return menu detail URL"""
    return reverse("menu:menu-detail", args=[menu_id])


def sample_menu(user, **params):
    """Create and return a sample menu"""
    defaults = {
        "main_dish": "Sample dish",
        "side_dish": "Side sample",
        "dessert": "Cake",
    }
    defaults.update(params)

    return Menu.objects.create(added_by_user=user, **defaults)


class PublicMenuAPITests(TestCase):
    """Test API requests for menus that do not require authentication"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(MENU_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMenuAPITests(TestCase):
    """Test API requests for menu that require authentication"""

    def setUp(self):
        self.user_payload = {
            "username": "supertestuser30",
            "password": "test123.@1",
        }
        self.user = create_staff_user(**self.user_payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_staff_permissions_for_user(self):
        """Test that user needs staff status to interact with this endpoint"""
        self.user_payload = {
            "username": "testuser30",
            "password": "test123.@1",
            "name": "test",
        }
        self.user = create_user(**self.user_payload)
        self.client.force_authenticate(user=self.user)
        res = self.client.get(MENU_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_menus(self):
        """Test that inserted menus are retrieved"""
        sample_menu(user=self.user)
        sample_menu(user=self.user)

        res = self.client.get(MENU_URL)

        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_menus_limited_to_user(self):
        """Test retrieving menus for user"""
        user2 = get_user_model().objects.create_superuser("otherstaff", "password123")
        sample_menu(user=user2)
        sample_menu(user=self.user)

        res = self.client.get(MENU_URL)

        menus = Menu.objects.filter(added_by_user=self.user)
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_creating_a_menu(self):
        """Test creating a new menu and checking the generated fields"""
        timezone.activate("America/Mexico_City")
        payload = {
            "main_dish": "Sample dish",
            "side_dish": "Side sample",
            "dessert": "Cake",
            "preparation_date": timezone.now().isoformat(),
        }

        res = self.client.post(MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            res.data["weekday"], parser.parse(res.data["preparation_date"]).isoweekday()
        )
        self.assertEqual(
            res.data["meal_time"],
            get_meal_time(parser.parse(res.data["preparation_date"]).hour),
        )
        timezone.deactivate()

    def test_partial_update_menu(self):
        """Test updating a menu with patch"""
        menu = sample_menu(user=self.user)

        payload = {"main_dish": "New main", "weekday": 3}
        url = detail_url(menu.id)
        self.client.patch(url, payload)
        menu.refresh_from_db()

        self.assertEqual(menu.main_dish, payload["main_dish"])
        self.assertEqual(menu.weekday, payload["weekday"])

    def test_get_menu_detail(self):
        """Test that the menu detail is returned"""
        menu = sample_menu(user=self.user)
        url = detail_url(menu.id)

        res = self.client.get(url)

        serializer = MenuDetailSerializer(menu)
        self.assertEqual(res.data, serializer.data)
