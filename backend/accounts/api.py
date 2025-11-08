from rest_framework import routers, viewsets, permissions
from django.urls import path, include
from django.contrib.auth.models import User
from .serializers import UserSerializer
class MeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all(); serializer_class = UserSerializer; permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return User.objects.filter(id=self.request.user.id)
router = routers.DefaultRouter(); router.register(r"me", MeViewSet, basename="me")
urlpatterns = [path("", include(router.urls))]
