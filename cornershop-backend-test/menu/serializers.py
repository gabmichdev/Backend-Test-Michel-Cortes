import datetime

from rest_framework import serializers

from core.models import Menu


def get_meal_time(hour):
    """Gets the meal time depending on the hour the meal
    was created for.

    Args:
        hour (int): Hour of the day from 0 to 23

    Returns:
        int: Meal time integer
    """
    # Breakfast
    if 6 <= hour < 12:
        return 1
    # Lunch
    if 12 <= hour < 18:
        return 2
    # Dinner
    if 18 <= hour:
        return 3
    # After
    elif 0 <= hour < 6:
        return 4


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for the menu object"""

    class Meta:
        model = Menu
        fields = (
            "id",
            "main_dish",
            "side_dish",
            "dessert",
            "preparation_date",
            "weekday",
            "meal_time",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        preparation_date: datetime.datetime = validated_data["preparation_date"]

        validated_data["weekday"] = preparation_date.isoweekday()
        validated_data["meal_time"] = get_meal_time(preparation_date.hour)
        menu = Menu.objects.create(**validated_data)
        return menu


class MenuDetailSerializer(MenuSerializer):
    """Serializer for details menu"""

    pass
