from rest_framework import serializers
from .models import Plan, Workout, Metric
class WorkoutSerializer(serializers.ModelSerializer):
    class Meta: model = Workout; fields = ["id","plan","date","kind","distance_km","duration_min","notes"]
class PlanSerializer(serializers.ModelSerializer):
    workouts = WorkoutSerializer(many=True, read_only=True)
    class Meta: model = Plan; fields = ["id","name","start_date","weeks","target_race","created_at","workouts"]
class MetricSerializer(serializers.ModelSerializer):
    class Meta: model = Metric; fields = ["id","date","weight_kg","rhr_bpm"]
