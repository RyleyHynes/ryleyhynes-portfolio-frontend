from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Peak, Route, TripPlan, AscentLog
from .serializers import PeakSerializer, RouteSerializer, TripPlanSerializer, AscentLogSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # works for TripPlan (has user) and AscentLog (plan.user)
        return getattr(obj, "user", getattr(getattr(obj, "plan", None), "user", None)) == request.user

class PeakViewSet(viewsets.ModelViewSet):
    queryset = Peak.objects.all()
    serializer_class = PeakSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["name", "region"]
    filterset_fields = ["region", "grade"]
    ordering = ["name"]

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("peak").all()
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["peak"]
    search_fields = ["name", "peak__name"]

class TripPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TripPlanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "route__peak"]

    def get_queryset(self):
        return TripPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AscentLogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = AscentLogSerializer

    def get_queryset(self):
        return AscentLog.objects.filter(plan__user=self.request.user)
