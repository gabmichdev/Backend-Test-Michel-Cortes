from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Menu, MenuSelection
from menu_selection.serializers import MenuSelectionSerializer

MENU_SELECTION_URL = reverse("menu_selection:menuselection-list")


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


def sample_menu_selection(user, **params):
    """Create and return a sample menu"""
    menu_item = {
        "main_dish": "Sample dish",
        "side_dish": "Side sample",
        "dessert": "Cake",
    }
    staff_user_payload = {
        "username": "testuser30",
        "password": "test123.@1",
    }
    staff_user = create_staff_user(**staff_user_payload)
    customizations = "This is a customization"
    menu_item.update(params)
    menu = Menu.objects.create(**menu_item, added_by_user=staff_user)
    selection = MenuSelection.objects.create(
        menu=menu, user=user, customizations=customizations
    )
    return selection


class PrivateMenuAPITests(TestCase):
    """Tests for the menu selection app"""

    def setUp(self):
        self.user_payload = {
            "username": "testuser301",
            "password": "test123.@1",
        }
        self.user = create_user(**self.user_payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_menu_selections(self):
        """Test that inserted menus are retrieved"""

        sample_menu_selection(self.user)
        res = self.client.get(MENU_SELECTION_URL)
        selections = MenuSelection.objects.all()
        serializer = MenuSelectionSerializer(selections, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_creating_a_menu_selection(self):
        """Test creating a new menu selection"""
        staff_user_payload = {
            "username": "testuser304",
            "password": "test123.@1",
        }
        staff_user = create_staff_user(**staff_user_payload)
        menu = sample_menu(staff_user)
        payload = {
            "menu": menu.id,
            "user": self.user,
            "customizations": "Cake de chocolate",
        }

        res = self.client.post(MENU_SELECTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
