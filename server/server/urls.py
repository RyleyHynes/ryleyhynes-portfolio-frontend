from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns = [
 path("admin/", admin.site.urls),
 path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
 path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
 path("api/accounts/", include("accounts.api")),
 path("api/tracker/", include("project_tracker.api")),
 path("api/training/", include("training.api")),
 path("api/shop/", include("shop.api")),
 path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
 path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
urlpatterns += [re_path(r"^(?!api/).*", TemplateView.as_view(template_name="index.html"))]
