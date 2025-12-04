from typing import Any
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class LiveFeedConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        app = self.scope['url_route']['kwargs'].get('app', 'all')
        group = f"livefeed_{app}"
        self.group_name = group
        await self.channel_layer.group_add(group, self.channel_name)

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: Any, **kwargs):
        pass

    async def stream_event(self, event):
        await self.send_json(event.get('data', {}))

