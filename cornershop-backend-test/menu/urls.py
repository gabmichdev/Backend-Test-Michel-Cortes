from django.urls import include, path
from rest_framework.routers import DefaultRouter

from menu.views import MenuViewSet

router = DefaultRouter()
router.register("menu", MenuViewSet)

app_name = "menu"

urlpatterns = [path("", include(router.urls))]
