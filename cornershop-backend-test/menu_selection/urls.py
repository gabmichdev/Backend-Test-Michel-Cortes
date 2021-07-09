from django.urls import include, path
from rest_framework.routers import DefaultRouter

from menu_selection.views import MenuSelectionViewSet

router = DefaultRouter()
router.register("menu_selection", MenuSelectionViewSet)

app_name = "menu_selection"

urlpatterns = [path("", include(router.urls))]
