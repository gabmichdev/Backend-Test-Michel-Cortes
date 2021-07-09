import datetime

from rest_framework import serializers

from core.models import Menu


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
        menu = Menu.objects.create(**validated_data)
        return menu


class MenuDetailSerializer(MenuSerializer):
    """Serializer for details menu"""

    pass
