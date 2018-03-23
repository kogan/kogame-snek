import json
import logging

from channels.consumer import AsyncWebsocketConsumer

log = logging.getLogger(__name__)


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'snek'
        self.room_group_name = '{}_game'.format(self.room_name)

        # Join game
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self):

        # Leave game
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from Websocket
    async def receive(self, direction):

        # Send direction update to room group
        await self.send(text_data=json.dumps({
            'direction': direction,
        }))

    # Send game data to room group after a Tick is processed
    async def game_update(self, event):

        # TODO - add information processed from Tick
        data = event
        players = data['something']
        board = None
        leaderboard = None

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'players': players,
            'board': board,
            'leaderboard': leaderboard,
        }))
