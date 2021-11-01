from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('chat/<int:pk>/', consumers.ChatsConsumer.as_asgi())
]
