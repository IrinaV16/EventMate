from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/chat/event/<int:event_id>/", consumers.ChatConsumer.as_asgi()),
]