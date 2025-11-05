from rest_framework import serializers
from .models import Board, Column, Card, Comment
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    class Meta: model = Comment; fields = ["id","author","author_username","body","created_at"]
class CardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta: model = Card; fields = ["id","column","title","description","position","assignee","created_at","updated_at","comments"]
class ColumnSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    class Meta: model = Column; fields = ["id","board","name","position","cards"]
class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)
    class Meta: model = Board; fields = ["id","name","owner","created_at","columns"]
