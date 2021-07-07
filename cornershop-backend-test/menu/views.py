from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from core.models import Menu
from menu.serializers import MenuDetailSerializer, MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    """Manage menus in the database"""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(added_by_user=self.request.user).order_by(
            "-weekday"
        )

    def perform_create(self, serializer):
        """Create a new menu object"""
        serializer.save(added_by_user=self.request.user)
        # Have to override save behavior because
        # menu belongs to authenticated user
        # authentication class takes care of getting the authenticated user
        # and assigning it to request so we can get self.request.user

    def get_serializer_class(self):
        """Return appropiate serializer class"""
        if self.action == "retrieve":
            return MenuDetailSerializer

        return MenuSerializer
