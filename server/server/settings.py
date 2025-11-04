from pathlib import Path
import os
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY","dev-not-secret")
DEBUG = os.environ.get("DJANGO_DEBUG","1") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS","localhost,127.0.0.1").split(",")
INSTALLED_APPS = [
 "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
 "rest_framework","corsheaders","drf_spectacular",
 "common","accounts","project_tracker","training","shop",
]
MIDDLEWARE = [
 "django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware","corsheaders.middleware.CorsMiddleware",
 "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
 "django.contrib.sessions.middleware.SessionMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "server.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR / "templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":[
 "django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="server.wsgi.application"
ASGI_APPLICATION="server.asgi.application"
DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR / "db.sqlite3"}}
LANGUAGE_CODE="en-us"; TIME_ZONE="UTC"; USE_I18N=True; USE_TZ=True
STATIC_URL="/static/"; STATIC_ROOT=BASE_DIR / "static"
STORAGES={"staticfiles":{"BACKEND":"whitenoise.storage.CompressedManifestStaticFilesStorage"}}
CORS_ALLOWED_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]; CORS_ALLOW_CREDENTIALS=True
REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":("rest_framework_simplejwt.authentication.JWTAuthentication",),"DEFAULT_PERMISSION_CLASSES":("rest_framework.permissions.IsAuthenticatedOrReadOnly",),"DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema"}
SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),"REFRESH_TOKEN_LIFETIME": timedelta(days=7),"AUTH_HEADER_TYPES": ("Bearer",)}
SPECTACULAR_SETTINGS={"TITLE":"Portfolio API","DESCRIPTION":"Project Tracker, Training Planner, Shop","VERSION":"1.0.0"}
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")
CSRF_TRUSTED_ORIGINS=[f"https://{h}" for h in ALLOWED_HOSTS if h not in ("localhost","127.0.0.1")]
