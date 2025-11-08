"""_summary_"""
from rest_framework import serializers
from .models import Peak, Route, TripPlan, AscentLog

class PeakSerializer(serializers.ModelSerializer):
    """Serializer for Peak model."""
    class Meta:
        """_summary_
        """
        model = Peak
        fields = '__all__'
class RouteSerializer(serializers.ModelSerializer):
    """Serializer for Route model."""
    peak = PeakSerializer(read_only=True)
    peak_id = serializers.PrimaryKeyRelatedField(source='peak', queryset=Peak.objects.all(), write_only=True)
    class Meta:
        """_summary_
        """
        model = Route
        fields = ('id', 'name', 'distance_mi', 'vert_gain_ft', 'season', 'notes')
class TripPlanSerializer(serializers.ModelSerializer):
    """Serializer for TripPlan model."""
    class Meta:
        """_summary_
        """
        model = TripPlan
        fields = '__all__'
class AscentLogSerializer(serializers.ModelSerializer):
    """Serializer for AscentLog model."""
    class Meta: 
        """_summary_
        """
        model = AscentLog
        fields = '__all__'