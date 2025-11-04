from rest_framework import viewsets, permissions, routers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.urls import path, include
from django.db.models import Sum, Avg
from .models import Plan, Workout, Metric
from .serializers import PlanSerializer, WorkoutSerializer, MetricSerializer
from .services import generate_plan
class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer; permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self): return Plan.objects.filter(owner=self.request.user).prefetch_related("workouts")
    @action(detail=False, methods=["post"])
    def generate(self, request):
        plan = generate_plan(request.user, request.data.get("name","Training Plan"), request.data.get("start_date"), int(request.data.get("weeks",12)))
        return Response(PlanSerializer(plan).data, status=status.HTTP_201_CREATED)
class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer; permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self): return Workout.objects.filter(plan__owner=self.request.user)
class MetricViewSet(viewsets.ModelViewSet):
    serializer_class = MetricSerializer; permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self): return Metric.objects.filter(owner=self.request.user)
    def perform_create(self, serializer): serializer.save(owner=self.request.user)
class StatsViewSet(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated]
    def list(self, request):
        total_km = Workout.objects.filter(plan__owner=request.user).aggregate(Sum("distance_km"))["distance_km__sum"] or 0
        avg_rhr = Metric.objects.filter(owner=request.user).aggregate(Avg("rhr_bpm"))["rhr_bpm__avg"]
        return Response({"total_km": total_km, "avg_rhr": avg_rhr})
router=routers.DefaultRouter()
router.register(r"plans", PlanViewSet, basename="plan")
router.register(r"workouts", WorkoutViewSet, basename="workout")
router.register(r"metrics", MetricViewSet, basename="metric")
router.register(r"stats", StatsViewSet, basename="stats")
urlpatterns=[path("", include(router.urls))]
