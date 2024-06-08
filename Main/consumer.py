import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Message_Chats

class Notification(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'notify'
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

    async def send_notification(self, event):
        # Retrieve necessary data from the event
        notification = event['notification']

        # Send notification to connected clients
        await self.send(text_data=json.dumps(notification))

class Chat_doctor(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, code):
        # get out of room
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)
        return
    
    async def recive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            session = data['session']
            sender = data['sender']
            receiver = data['receiver']
            message_attach = data['attach']

            user = await self.get_user()
            if user.is_authenticated:
                await self.save_message(
                    user,
                    message if message !='' else None,
                    message_attach if message_attach !='' else None,
                    session,
                    sender,
                    receiver
                )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'send_msg',
                    'message':message,
                    'session':str(session),
                    'sender':sender,
                    'receiver':receiver,
                    'attach':message_attach
                }
            )
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON : {e}')

    async def send_msg(self , event):
        message = event['message']
        attach = event['attach']
        sender = event['sender']
        receiver = event['receiver']
        session = event['session']

        await self.send(text_data=json.dumps({
            'message':message,
            'session':str(session),
            'sender':sender,
            'receiver':receiver,
            'attach':attach
        }))

    @database_sync_to_async
    def save_message(self , user , msg , attach , session , sender , receiver):
        if user.is_authenticated and user.profile.pk == sender:
            if msg and attach:
                x = Message_Chats(
                    sender = sender,
                    receiver = receiver,
                    last_message = msg,
                    message = msg,
                    attach = attach,
                    session = session
                )
                x.save()
            elif attach and msg == None:
                x = Message_Chats(
                    sender = sender,
                    receiver = receiver,
                    last_message = 'attachment',
                    attach = attach,
                    session = session
                )
                x.save()
            elif msg and attach == None:
                x = Message_Chats(
                    sender = sender,
                    receiver = receiver,
                    last_message = msg,
                    message = msg,
                    session = session
                )
                x.save()

    @database_sync_to_async
    def get_user(self):
        return self.scope['user']

            
