from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Peak, Route, TripPlan, AscentLog
from .serializers import PeakSerializer, RouteSerializer, TripPlanSerializer, AscentLogSerializer
from .data_sources import (
    OsmError,
    OsmNotFound,
    WeatherError,
    apply_osm_snapshot,
    fetch_osm_snapshot_for_peak,
    fetch_weather_forecast,
    search_osm_peaks,
)

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

    def _snapshot_payload(self, peak: Peak):
        return {
            "source": peak.external_source,
            "external_id": peak.external_id,
            "country": peak.external_country,
            "range": peak.external_range,
            "elevation_m": peak.external_elevation_m,
            "prominence_m": peak.external_prominence_m,
            "retrieved_at": peak.external_retrieved_at.isoformat() if peak.external_retrieved_at else None,
            "payload": peak.external_payload,
        }

    @action(detail=True, methods=["post"], url_path="osm/refresh")
    def refresh_osm_snapshot(self, request, pk=None):
        peak = self.get_object()
        force = request.query_params.get("force", "true").lower() in {"1", "true", "yes"}
        try:
            snapshot, from_cache = fetch_osm_snapshot_for_peak(peak, force_refresh=force)
            apply_osm_snapshot(peak, snapshot)
        except OsmNotFound as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except OsmError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "peak": self.get_serializer(peak).data,
                "snapshot": self._snapshot_payload(peak),
                "from_cache": from_cache,
            }
        )

    @action(detail=False, methods=["get"], url_path="osm/search")
    def search_osm_action(self, request):
        query = request.query_params.get("q", "").strip()
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        radius = request.query_params.get("radius", 50000)
        try:
            limit = int(request.query_params.get("limit", 5))
        except ValueError:
            return Response({"detail": "Limit must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            radius = int(radius)
        except ValueError:
            return Response({"detail": "Radius must be an integer (meters)."}, status=status.HTTP_400_BAD_REQUEST)

        def _parse_coord(value):
            if value is None or value == "":
                return None
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"Invalid coordinate '{value}'")

        try:
            lat_f = _parse_coord(lat)
            lon_f = _parse_coord(lon)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            snapshots = search_osm_peaks(query or None, lat=lat_f, lon=lon_f, radius_m=radius, limit=limit)
        except OsmNotFound as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except (OsmError, ValueError) as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        for snap in snapshots:
            results.append(
                {
                    "osm_id": snap.osm_id,
                    "name": snap.name,
                    "lat": snap.lat,
                    "lon": snap.lon,
                    "elevation_m": snap.elevation_m,
                    "country": snap.country,
                    "region": snap.region,
                    "range": snap.range,
                    "retrieved_at": snap.retrieved_at.isoformat(),
                }
            )
        return Response({"results": results})

    @action(detail=True, methods=["get"], url_path="weather")
    def peak_weather(self, request, pk=None):
        peak = self.get_object()
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")

        try:
            lat = float(lat) if lat is not None else float(peak.lat) if peak.lat is not None else None
            lon = float(lon) if lon is not None else float(peak.lon) if peak.lon is not None else None
        except (TypeError, ValueError):
            return Response({"detail": "lat/lon must be numeric."}, status=status.HTTP_400_BAD_REQUEST)

        if lat is None or lon is None:
            return Response({"detail": "Peak is missing coordinates. Add lat/lon first."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            forecast = fetch_weather_forecast(lat, lon)
        except WeatherError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({"forecast": forecast, "peak": self.get_serializer(peak).data})

    @action(detail=False, methods=["get"], url_path="weather")
    def ad_hoc_weather(self, request):
        try:
            lat = float(request.query_params.get("lat"))
            lon = float(request.query_params.get("lon"))
        except (TypeError, ValueError):
            return Response({"detail": "lat and lon query parameters are required and must be numeric."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            forecast = fetch_weather_forecast(lat, lon)
        except WeatherError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({"forecast": forecast})

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
