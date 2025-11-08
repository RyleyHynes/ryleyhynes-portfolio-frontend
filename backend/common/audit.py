from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()
class AuditLog(models.Model):
    actor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=50)
    entity = models.CharField(max_length=50)
    entity_id = models.IntegerField()
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=now, db_index=True)
    class Meta: ordering = ["-created_at"]
