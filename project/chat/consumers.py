import json

from django.core.checks import messages
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.contenttypes.models import ContentType
from channels.db import database_sync_to_async
from chat.models import Room, Message


class ChatsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """Create websocket connection """

        self.chat_id = self.scope['url_route']['kwargs']['pk']
        self.chat_group_name = 'chat_%s' % self.chat_id

        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """ Receive messages from client"""
        text_data_json = json.loads(text_data)
        message = text_data_json['text']

        new_message = await self.create_new_message(message)

        data = {
            'author': new_message.author.username,
            'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%m'),
            'body': new_message.body,
        }


        """ send received messages to all connected users"""
        await self.channel_layer.group_send(
                                    self.chat_group_name,
                                    {
                                        'type': 'new_message',
                                        'message': data
                                    }
                                )

    async def new_message(self, event):
        message = event['message']
        await self.send(
            text_data=json.dumps({
                'message': message,
            })
        )

    @database_sync_to_async
    def create_new_message(self, text):
        """Create message model object"""

        room = Room.objects.get(pk=self.chat_id)
        author = self.scope['user']
        recipient = author.message_delivered.filter(room=room)[0].author

        new_message = Message.objects.create(author=author,
                                             recipient=recipient, 
                                             room=room, body=text)

        return new_message
