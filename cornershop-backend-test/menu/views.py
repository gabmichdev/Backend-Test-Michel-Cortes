from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import SAFE_METHODS, BasePermission

from core.models import Menu
from core.utils.date_utils import generate_day_range_for_date
from menu.serializers import MenuDetailSerializer, MenuSerializer


class IsAuthenticatedStaffOrReadOnly(BasePermission):
    """Safe requests are open an unauthenticated but unsafe are made by staff"""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class MenuViewSet(viewsets.ModelViewSet):
    """Manage menus in the database"""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedStaffOrReadOnly,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        preparation_date = self.request.query_params.get("preparation_date")
        order_by = self.request.query_params.get("order_by") or "weekday"
        sort = self.request.query_params.get("sort") or ""
        sort = "-" if sort == "desc" else ""

        if preparation_date:
            gte, lte = generate_day_range_for_date(preparation_date)
            self.queryset = self.queryset.filter(
                preparation_date__gte=gte,
                preparation_date__lte=lte,
            )

        return self.queryset.order_by(f"{sort}{order_by}")

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
