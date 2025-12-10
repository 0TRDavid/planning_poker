from channels.generic.websocket import AsyncWebsocketConsumer
import json


# WEBSOCKET non utilisé pour l'instant mais à garder pour une évolution future en temps réel

class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        await self.channel_layer.group_add(
            self.session_id,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.session_id,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Traitez les données (vote, nouveau joueur, etc.)
        await self.channel_layer.group_send(
            self.session_id,
            {
                'type': 'session_message',
                'message': data
            }
        )

    async def session_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))