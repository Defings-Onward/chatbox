import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = f"room_{self.scope['url_route']['kwargs']['room_id']}"
        await self.channel_layer.group_add(self.room_id, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_id, self.channel_name)
        self.close(code)

    async def receive(self, text_data):
        # print("Recieved Data")
        data_json = json.loads(text_data)
        # print(data_json)

        event = {"type": "send_message", "message": data_json}

        await self.channel_layer.group_send(self.room_id, event)

    async def send_message(self, event):
        data = event["message"]
        await self.create_message(data=data)

        response = {"sender": data["sender"], "message": data["message"]}

        await self.send(text_data=json.dumps({"message": response}))

    @database_sync_to_async
    def create_message(self, data):
        get_room = Room.objects.get(id=data["room_id"])
        get_user = User.objects.get(username=data["sender"])
        if not Message.objects.filter(
            message=data["message"], sender=get_user
        ).exists():
            new_message = Message.objects.create(
                room=get_room, message=data["message"], sender=get_user
            )
