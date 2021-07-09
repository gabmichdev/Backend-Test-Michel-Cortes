from rest_framework import serializers

from core.models import MenuSelection


class MenuSelectionSerializer(serializers.ModelSerializer):
    """Serializer for the menu selection modelobject"""

    class Meta:
        model = MenuSelection
        fields = (
            "customizations",
            "menu",
        )

    def create(self, validated_data):
        """Create a menu selection"""
        menu_selection = MenuSelection.objects.create(**validated_data)
        return menu_selection


class MenuSelectionDetailSerializer(MenuSelectionSerializer):
    """Serializer for details menu selection"""

    pass
    # menu = MenuSerializer(read_only=True)
    # user = UserSerializer(read_only=True)
