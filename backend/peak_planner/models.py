"""Peak Planner Models."""
from django.db import models
from django.conf import settings
class Peak (models.Model):
    """Model representing a mountain peak."""
    name = models.CharField(max_length=100, unique= True)
    region= models.CharField(max_length=100)
    elevation_ft = models.IntegerField()
    lat = models.FloatField()
    lon= models.FloatField()
    def _str_(self):
        return self.name
    
class Route(models.Model):
    """Model representing a climbing route on a peak."""
    peak = models.ForeignKey(Peak, on_delete= models.CASCADE, related_name='routes')
    name = models.CharField(max_length=120)
    distance_mi = models.FloatField(null=True, blank=True)
    vert_gain_ft = models.FloatField(null=True, blank=True)
    season = models.CharField(max_length=80, blank=True)
    notes=models.TextField(blank=True)
    class Meta: 
        """_summary_
        """
        unique_together = ('peak', 'name')

class TripPlan(models.Model):
    """Model representing a trip plan for climbing a peak."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plans')
    route= models.ForeignKey(Route, on_delete=models.CASCADE, related_name='plans')
    start_date = models.DateField()
    end_date = models.DateField()
    team_size = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, default='planned') # planned|attempted|summited|bailed
    objective_hazards = models.TextField(blank=True) # crevasses, rockfall, ect.

class AscentLog(models.Model):
    """Model representing an ascent log for a completed climb."""
    plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name='ascents')
    outcome = models.CharField(max_length=20) # e.g., summited|bailed
    time_hours = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)