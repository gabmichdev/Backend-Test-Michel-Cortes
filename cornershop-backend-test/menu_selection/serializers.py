from datetime import datetime

from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from core.models import Menu, MenuSelection
from core.utils.date_utils import generate_day_range_for_date, is_between
from users.serializers import UserSerializer
from django.utils.translation import ugettext_lazy as _


class ValidationError422(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class MenuSelectionSerializer(serializers.ModelSerializer):
    """Serializer for the menu selection modelobject"""

    class Meta:
        model = MenuSelection
        fields = ("customizations", "menu", "user")

    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        """Create a menu selection"""
        menu_selection = MenuSelection.objects.create(**validated_data)
        return menu_selection

    def validate(self, data):
        """
        Check that start is before finish.
        """
        menu_id = data["menu"].id
        now = timezone.now()
        hour = now.hour
        gte, lte = generate_day_range_for_date(now)
        menu = Menu.objects.get(id=menu_id)
        valid_selection = is_between(menu.preparation_date, lte, gte)
        # Check menu selected is for today
        errors = []
        if not valid_selection:
            errors.append(_("El menu seleccionado no es del dia de hoy"))
        if not hour < 11:
            errors.append(_("No puedes seleccionar un menu despues de las 11 AM"))
        if errors:
            raise serializers.ValidationError(detail={"menu": errors})
        return data
