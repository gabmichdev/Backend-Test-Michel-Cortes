from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import MenuSelection
from core.utils.date_utils import generate_day_range_for_date
from menu_selection.serializers import MenuSelectionSerializer


class MenuSelectionViewSet(viewsets.ModelViewSet):
    """Manage menus in the database"""

    queryset = MenuSelection.objects.all()
    serializer_class = MenuSelectionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        selected_at = self.request.query_params.get("selected_at")
        order_by = self.request.query_params.get("order_by") or "selected_at"
        sort = self.request.query_params.get("sort") or ""
        sort = "-" if sort == "desc" else ""

        if selected_at:
            gte, lte = generate_day_range_for_date(selected_at)
            self.queryset = self.queryset.filter(
                preparation_date__gte=gte,
                preparation_date__lte=lte,
            )
        is_staff = self.request.user.is_staff
        if not is_staff:
            self.queryset = self.queryset.filter(user=self.request.user)

        return self.queryset.order_by(f"{sort}{order_by}")

    def perform_create(self, serializer):
        """Create a new menu object"""
        serializer.save(user=self.request.user)

    def retrieve(self, request):
        return self.queryset.get(user=request.user)
