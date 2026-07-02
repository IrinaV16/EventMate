import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from events.models import Event
from .models import ChatMessage

from applications.models import Application


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.event_id = self.scope["url_route"]["kwargs"]["event_id"]
        self.room_group_name = f"chat_event_{self.event_id}"

        user = self.scope["user"]

        event = await sync_to_async(Event.objects.get)(id=self.event_id)

        is_organizer = event.organizer_id == user.id

        is_accepted = await sync_to_async(
            Application.objects.filter(
                event=event,
                applicant=user,
                status="accepted"
            ).exists
        )()

        if not is_organizer and not is_accepted:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        user = self.scope["user"]

        chat_message = await self.save_message(user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": chat_message.message,
                "username": user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))

    @sync_to_async
    def save_message(self, user, message):
        event = Event.objects.get(id=self.event_id)

        return ChatMessage.objects.create(
            event=event,
            sender=user,
            message=message
        )