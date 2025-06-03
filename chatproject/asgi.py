import os
from django.core.asgi import get_asgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatproject.settings")

from channels.routing import ProtocolTypeRouter, URLRouter
from chatapp.routing import wsPattern



http_response_app = get_asgi_application()

application = ProtocolTypeRouter(
    {"http": http_response_app, "websocket": URLRouter(wsPattern)}
)
