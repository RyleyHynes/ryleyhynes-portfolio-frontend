from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth (JWT)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # App APIs (each app exposes `urlpatterns` in its api.py)
    path("api/profile/", include("profile.api")),
    path("api/peaks/", include("peak_planner.api")),        # or project_tracker.api if that’s your name
    path("api/routes/", include("route_log.api")),
    path("api/supplies/", include("trail_supply.api")),

    # OpenAPI + Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

# Optional SPA catch-all if Django serves your built React index.html
urlpatterns += [
    re_path(r"^(?!api/).*", TemplateView.as_view(template_name="index.html"))
]
