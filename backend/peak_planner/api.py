from rest_framework.routers import DefaultRouter
from .views import PeakViewSet, RouteViewSet, TripPlanViewSet, AscentLogViewSet

router = DefaultRouter()
router.register("peaks", PeakViewSet, basename="peak")
router.register("routes", RouteViewSet, basename="route")
router.register("plans", TripPlanViewSet, basename="plan")
router.register("ascents", AscentLogViewSet, basename="ascent")

urlpatterns = router.urls
