"""Serializers for the Peak Planner domain."""

from rest_framework import serializers

from .models import AscentLog, Peak, Route, TripPlan


class PeakSerializer(serializers.ModelSerializer):
  """Serializer for Peak model."""

  lat = serializers.DecimalField(max_digits=9, decimal_places=6, allow_null=True, required=False, coerce_to_string=False)
  lon = serializers.DecimalField(max_digits=9, decimal_places=6, allow_null=True, required=False, coerce_to_string=False)

  class Meta:
    model = Peak
    fields = [
        "id",
        "name",
        "region",
        "grade",
        "elevation_ft",
        "prominence_ft",
        "lat",
        "lon",
        "description",
        "external_source",
        "external_id",
        "external_country",
        "external_range",
        "external_elevation_m",
        "external_prominence_m",
        "external_retrieved_at",
        "external_payload",
        "created_at",
        "updated_at",
    ]
    read_only_fields = ["id", "created_at", "updated_at"]


class RouteSerializer(serializers.ModelSerializer):
  """Serializer for Route model."""

  peak = PeakSerializer(read_only=True)
  peak_id = serializers.PrimaryKeyRelatedField(
      source="peak", queryset=Peak.objects.all(), write_only=True
  )
  distance_mi = serializers.DecimalField(max_digits=6, decimal_places=2, allow_null=True, required=False, coerce_to_string=False)

  class Meta:
    model = Route
    fields = [
        "id",
        "peak",
        "peak_id",
        "name",
        "distance_mi",
        "vert_gain_ft",
        "grade",
        "season",
        "notes",
        "created_at",
        "updated_at",
    ]
    read_only_fields = ["id", "created_at", "updated_at", "peak"]


class TripPlanSerializer(serializers.ModelSerializer):
  """Serializer for TripPlan model."""

  route = RouteSerializer(read_only=True)
  route_id = serializers.PrimaryKeyRelatedField(
      source="route", queryset=Route.objects.all(), write_only=True
  )

  class Meta:
    model = TripPlan
    fields = [
        "id",
        "user",
        "route",
        "route_id",
        "start_date",
        "end_date",
        "team_size",
        "status",
        "objectives",
        "notes",
        "created_at",
        "updated_at",
    ]
    read_only_fields = ["id", "user", "created_at", "updated_at", "route"]


class AscentLogSerializer(serializers.ModelSerializer):
  """Serializer for AscentLog model."""

  plan = TripPlanSerializer(read_only=True)
  plan_id = serializers.PrimaryKeyRelatedField(
      source="plan", queryset=TripPlan.objects.all(), write_only=True
  )

  class Meta:
    model = AscentLog
    fields = [
        "id",
        "plan",
        "plan_id",
        "outcome",
        "time_hours",
        "notes",
        "recorded_at",
        "created_at",
        "updated_at",
    ]
    read_only_fields = ["id", "created_at", "updated_at", "plan", "recorded_at"]
