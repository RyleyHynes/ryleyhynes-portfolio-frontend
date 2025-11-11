"""Peak Planner domain models."""

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
  """Reusable created/updated timestamps."""

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True


class Peak(TimeStampedModel):
  """Mountain peak available to plan ascents for."""

  name = models.CharField(max_length=120, unique=True)
  region = models.CharField(max_length=120, blank=True)
  elevation_ft = models.PositiveIntegerField(null=True, blank=True)
  prominence_ft = models.PositiveIntegerField(null=True, blank=True)
  grade = models.CharField(max_length=32, blank=True)
  lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
  lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
  description = models.TextField(blank=True)
  external_source = models.CharField(max_length=50, blank=True)
  external_id = models.CharField(max_length=120, blank=True)
  external_country = models.CharField(max_length=120, blank=True)
  external_range = models.CharField(max_length=120, blank=True)
  external_elevation_m = models.PositiveIntegerField(null=True, blank=True)
  external_prominence_m = models.PositiveIntegerField(null=True, blank=True)
  external_retrieved_at = models.DateTimeField(null=True, blank=True)
  external_payload = models.JSONField(null=True, blank=True)

  class Meta:
    ordering = ["name"]

  def __str__(self) -> str:
    return self.name


class Route(TimeStampedModel):
  """Individual route on a given peak."""

  peak = models.ForeignKey(Peak, on_delete=models.CASCADE, related_name="routes")
  name = models.CharField(max_length=120)
  distance_mi = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
  vert_gain_ft = models.PositiveIntegerField(null=True, blank=True)
  grade = models.CharField(max_length=32, blank=True)
  season = models.CharField(max_length=80, blank=True)
  notes = models.TextField(blank=True)

  class Meta:
    ordering = ["peak__name", "name"]
    unique_together = ("peak", "name")

  def __str__(self) -> str:
    return f"{self.name} ({self.peak.name})"


class TripPlan(TimeStampedModel):
  """Trip plan for attempting a route on a peak."""

  class Status(models.TextChoices):
    PLANNED = ("planned", "Planned")
    IN_PROGRESS = ("in_progress", "In Progress")
    READY = ("ready", "Ready")
    COMPLETED = ("completed", "Completed")
    CANCELED = ("canceled", "Canceled")

  user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name="peak_trip_plans",
  )
  route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="plans")
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  team_size = models.PositiveSmallIntegerField(default=1)
  status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
  objectives = models.TextField(blank=True)
  notes = models.TextField(blank=True)

  class Meta:
    ordering = ["-start_date"]

  def __str__(self) -> str:
    return f"{self.route.peak.name} – {self.route.name}"


class AscentLog(TimeStampedModel):
  """Log entry describing an ascent outcome for a trip plan."""

  plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name="ascents")
  outcome = models.CharField(max_length=20, blank=True)  # e.g., summited|bailed
  time_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
  notes = models.TextField(blank=True)
  recorded_at = models.DateField(auto_now_add=True)

  class Meta:
    ordering = ["-recorded_at"]

  def __str__(self) -> str:
    return f"Ascent for {self.plan}"
