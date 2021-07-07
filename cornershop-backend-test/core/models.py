from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import ugettext as _


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra):
        """Creates and saves new user"""
        user = self.model(username=username, **extra)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """Creates and saves super user"""
        user = self.create_user(username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model class"""

    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"


class CapitalField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(CapitalField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).capitalize()


class Menu(models.Model):
    """Menu item for a certain day"""

    DOW_CHOICES = (
        (1, _("Lunes")),
        (2, _("Martes")),
        (3, _("Miercoles")),
        (4, _("Jueves")),
        (5, _("Viernes")),
        (6, _("Sabado")),
        (7, _("Domingo")),
    )
    MEAL_TIMES = (
        (1, _("Desayuno")),
        (2, _("Comida")),
        (3, _("Cena")),
        (4, _("After")),
    )
    day = models.PositiveSmallIntegerField(
        choices=DOW_CHOICES, default=datetime.today().isoweekday()
    )
    main_dish = CapitalField(max_length=255)
    side_dish = CapitalField(max_length=255)
    dessert = CapitalField(max_length=255)
    meal_time = models.PositiveSmallIntegerField(choices=MEAL_TIMES, default=2)
    added_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        null=True,
        to_field="username",
    )