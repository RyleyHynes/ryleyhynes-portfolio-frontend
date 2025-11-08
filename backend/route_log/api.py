from rest_framework import routers
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r"boards", BoardViewSet, basename="board")
router.register(r"columns", ColumnViewSet, basename="column")
router.register(r"cards", CardViewSet, basename="card")
router.register(r"comments", CommentViewSet, basename="comment")
urlpatterns = [path("", include(router.urls))]
