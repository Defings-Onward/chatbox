from django.urls import path
from .consumers import ChatConsumer

wsPattern = [path("ws/messages/<str:room_id>/", ChatConsumer.as_asgi())]
