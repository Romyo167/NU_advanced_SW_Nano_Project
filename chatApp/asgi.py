# d:\Term-4\Advanced sw\Nan-Project-Phase-1\NU_advanced_SW_Nano_Project\chatApp\asgi.py
import os
from django.core.asgi import get_asgi_application

# Fetch Django ASGI application early to ensure AppRegistry is populated
# before importing consumers and AuthMiddlewareStack that may import ORM
# models.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatApp.settings')
django_asgi_app = get_asgi_application() # Keep this

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack # Import AuthMiddlewareStack
import myapp.routing # Import your app's routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app, # Use the Django ASGI app for HTTP requests
        "websocket": AuthMiddlewareStack( # Wrap WebSocket routing
            URLRouter(myapp.routing.websocket_urlpatterns)
        ),
    }
)
