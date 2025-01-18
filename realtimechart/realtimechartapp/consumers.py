import json
import os
from asyncio import sleep
from asgiref.sync import async_to_sync
from numpy.ma.core import append
import datetime
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async


class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'ws_stock'
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave user notification group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name)
        print(f"WebSocket disconnected with close code {close_code}")

    async def send_stock_data(self,event):
        data = event['message']
        print("yes--",data)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'data': data
        }))

