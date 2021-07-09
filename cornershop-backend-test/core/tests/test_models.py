from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Menu, MenuSelection


def sample_user(username="test123", password="test123"):
    """Create sample user"""
    return get_user_model().objects.create_user(username=username, password=password)


class UserModelTests(TestCase):
    """Tests for the user model"""

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


class MenuModelTests(TestCase):
    """Tests for the menu model"""

    def test_dishes_are_capitalized(self):
        """Test that the names of the dishes are capitalized"""
        menu_item = {
            "main_dish": "pechuga de pavo",
            "side_dish": "pure de papa",
            "dessert": "pastel",
            "added_by_user": sample_user(),
        }

        Menu.objects.create(**menu_item)
        menu = Menu.objects.get(main_dish=menu_item["main_dish"].capitalize())
        self.assertEqual(menu_item["main_dish"].capitalize(), menu.main_dish)
        self.assertEqual(menu_item["side_dish"].capitalize(), menu.side_dish)
        self.assertEqual(menu_item["dessert"].capitalize(), menu.dessert)

    def test_day_number_corresponds_if_not_specified(self):
        """
        Test that the day number corresponds correctly
        to todays if left blank
        """
        menu_item = {
            "main_dish": "pechuga de pavo",
            "side_dish": "pure de papa",
            "dessert": "pastel",
            "added_by_user": sample_user(),
        }

        menu = Menu.objects.create(**menu_item)
        today = datetime.today().isoweekday()

        self.assertEqual(menu.weekday, today)

    def test_inserting_field_with_human_readable_string_raises_error(self):
        """Test creating menu with human readable string for field gives
        error"""
        menu_item = {
            "main_dish": "pechuga de pavo",
            "side_dish": "pure de papa",
            "dessert": "pastel",
            "added_by_user": sample_user(),
            "meal_time": "Desayuno",
        }
        self.assertRaises(ValueError, Menu.objects.create, **menu_item)


class MenuSelectionModelTests(TestCase):
    """Tests for the menu selection model"""

    def test_user_is_saved_when_register_menu(self):
        """Test that the user that created the menu is the one saved"""
        menu_item = {
            "main_dish": "pechuga de pavo",
            "side_dish": "pure de papa",
            "dessert": "pastel",
            "added_by_user": sample_user(),
            "meal_time": 1,
        }
        menu = Menu.objects.create(**menu_item)
        user = menu_item["added_by_user"]

        menu_selection_item = {
            "menu": menu,
            "user": user,
            "customizations": "Agregar dos porciones del pure de papa",
        }
        menu_selection = MenuSelection.objects.create(**menu_selection_item)
        self.assertEqual(user, menu_selection.user)
        self.assertEqual(menu, menu_selection.menu)
