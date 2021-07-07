from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Menu
from users.serializers import UserSerializer


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for the menu object"""

    class Meta:
        model = Menu
        fields = (
            "id",
            "main_dish",
            "side_dish",
            "dessert",
            "meal_time",
            "day",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return super().create(validated_data)


class MenuDetailSerializer(MenuSerializer):
    """Serializer for details menu"""

    pass