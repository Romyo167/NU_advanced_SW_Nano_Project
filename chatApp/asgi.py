import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import myapp.routing  # Ensure "myapp" is used instead of "ws_app"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatApp.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(myapp.routing.websocket_urlpatterns)  # Ensure "myapp" is used here
    ),
})
