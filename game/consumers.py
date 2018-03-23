import logging

from channels.generic.websocket import JsonWebsocketConsumer
from channels.consumer import SyncConsumer

from .engine import GameEngine
from .models import Game

from .players import Direction, set_player_direction

log = logging.getLogger(__name__)


class PlayerConsumer(JsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'snek_game'
        self.game = None

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
                'id': 'get_user(whatevs).email',
                'channel': self.channel_name,
            }
        )

    async def disconnect(self):
        # Leave game
        log.info('Disconnect')
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from Websocket
    async def receive_json(self, content):
        log.info('Receive JSON: %s', content)
        direction = content['direction']
        await self.channel_layer.send(
            'game_engine',
            {
                'type': 'player.direction',
                'player': 'me',
                'direction': direction,
            }
        )

    # Send game data to room group after a Tick is processed
    async def game_update(self, event):
        log.info('Game Update: %s', event)
        # Send message to WebSocket
        state = event['state']
        await self.send_json(state)

    async def current_game(self, event):
        game_id = event['game_id']
        self.game = Game.objects.get(pk=game_id)


class GameConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        log.info('Game Consumer: %s %s', args, kwargs)
        super().__init__(*args, **kwargs)
        self.group_name = 'snek_game'
        self.game = Game.objects.create(tick=0)
        self.engine = GameEngine(self.game, self.group_name)
        self.engine.start()

    def player_new(self, event):
        log.info('Player Joined: %s', event)
        self.engine.player_new()

    def player_direction(self, event):
        log.info('Player direction changed: %s', event)
        direction = event.get('direction', 'UP')

        set_player_direction(
            self.game,
            event.get('player', 'Player 1'),
            Direction[direction]
        )
