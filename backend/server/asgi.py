import os
from pathlib import Path

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env.local')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
application = get_asgi_application()
