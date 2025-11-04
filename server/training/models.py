from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()
class Plan(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plans")
    name = models.CharField(max_length=120)
    start_date = models.DateField()
    weeks = models.PositiveIntegerField(default=12)
    target_race = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(default=now)
class Workout(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="workouts")
    date = models.DateField()
    kind = models.CharField(max_length=40)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    duration_min = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
class Metric(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rhr_bpm = models.PositiveIntegerField(null=True, blank=True)
