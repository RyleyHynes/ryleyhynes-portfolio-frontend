from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()
class Board(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards")
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(default=now)
class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    name = models.CharField(max_length=120)
    position = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["position","id"]
class Card(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="cards")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0)
    assignee = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["position","id"]
class Comment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(default=now)
