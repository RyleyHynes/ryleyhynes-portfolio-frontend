from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Board, Column, Card, Comment
from .serializers import BoardSerializer, ColumnSerializer, CardSerializer, CommentSerializer
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: return True
        owner = getattr(obj, "owner", None) or getattr(getattr(obj, "board", None), "owner", None)
        return owner == request.user
class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer; permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def get_queryset(self): return Board.objects.filter(owner=self.request.user).prefetch_related("columns__cards")
    def perform_create(self, serializer): serializer.save(owner=self.request.user)
class ColumnViewSet(viewsets.ModelViewSet):
    serializer_class = ColumnSerializer; permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Column.objects.select_related("board")
    @action(detail=True, methods=["post"])
    def move(self, request, pk=None):
        column = self.get_object()
        column.position = int(request.data.get("position", column.position)); column.save()
        return Response(self.get_serializer(column).data)
class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer; permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Card.objects.select_related("column","column__board")
    @action(detail=True, methods=["post"])
    def move(self, request, pk=None):
        card = self.get_object()
        with transaction.atomic():
            card.column_id = int(request.data.get("column", card.column_id))
            card.position = int(request.data.get("position", card.position))
            card.save()
        return Response(self.get_serializer(card).data)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer; permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self): return Comment.objects.filter(card__column__board__owner=self.request.user)
    def perform_create(self, serializer): serializer.save(author=self.request.user)