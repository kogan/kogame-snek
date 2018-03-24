import json
import logging

from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from .engine import Direction, GameEngine, join_queue, set_player_direction
from .models import Game

log = logging.getLogger(__name__)


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        log.info('Connect')
        scope = self.scope
        self.group_name = 'snek_game'
        self.game = None
        self.user = scope['user']
        log.info('User %s: Connected', self.user.email)

        # Join game
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        await self.channel_layer.send(
            'game_engine',
            {
                'type': 'player.new',
                'player': self.user.email,
                'channel': self.channel_name,
            }
        )

    async def disconnect(self, close_code):
        # Leave game
        log.info('Disconnect: %s', close_code)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from Websocket
    async def receive(self, text_data=None, bytes_data=None):
        log.info('Receive TEXT: %s', text_data)
        content = json.loads(text_data)
        update = content['updateObj']
        direction = update['direction']
        await self.channel_layer.send(
            'game_engine',
            {
                'type': 'player.direction',
                'player': self.user.email,
                'direction': direction,
            }
        )

    # Send game data to room group after a Tick is processed
    async def game_update(self, event):
        log.info('Game Update: %s', event)
        # Send message to WebSocket
        state = event['state']
        await self.send(json.dumps(state))


class GameConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        """
        Created on demand when the first player joins.
        """
        log.info('Game Consumer: %s %s', args, kwargs)
        super().__init__(*args, **kwargs)
        self.group_name = 'snek_game'
        self.game = Game.objects.create(tick=0)
        self.engine = GameEngine(self.game, self.group_name)
        self.engine.start()

    def player_new(self, event):
        log.info('Player Joined: %s', event['player'])
        join_queue(self.game, event['player'])

    def player_direction(self, event):
        log.info('Player direction changed: %s', event)
        direction = event.get('direction', 'UP')

        try:
            direction = Direction[direction]
        except KeyError:
            log.info('Bad Direction! %s', direction)
            return

        set_player_direction(self.game, event['player'], direction)
