import json
import logging

from channels.generic.websocket import JsonWebsocketConsumer
from channels.consumer import SyncConsumer

from .engine import GameEngine
from .models import Game

from .models import Game
from .players import Direction, get_player_directions, set_player_direction

log = logging.getLogger(__name__)


class PlayerConsumer(JsonWebsocketConsumer):
    async def connect(self):
        self.room_name = 'snek'
        self.room_group_name = '{}_game'.format(self.room_name)

        # Join game
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.channel_layer.send(
            'game_engine',
            {
                'type': 'player.new',
                'id': 'get_email_from_user',
                'channel': self.channel_name,
            }
        )

    async def disconnect(self):
        # Leave game
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from Websocket
    async def receive_json(self, content):
        direction = Direction[content['direction']]

        # update player direction
        set_player_direction(
            Game.current_board(),
            get_user(self.scope),
            direction
        )

    # Send game data to room group after a Tick is processed
    async def game_update(self, state):
        # Send message to WebSocket
        await self.send_json(state)


class GameConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        log.info('Game Consumer: %s %s', args, kwargs)
        super().__init__(*args, **kwargs)
        self.game = Game.objects.create(tick=0)
        self.engine = GameEngine(self.game)
        self.engine.start()
