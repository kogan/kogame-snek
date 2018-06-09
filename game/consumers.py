import json
import logging

from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from .engine import Direction, GameEngine

log = logging.getLogger(__name__)


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        log.info("Connect")
        self.group_name = "snek_game"
        self.game = None
        self.username = None
        log.info("User Connected")

        # Subscribe to game state
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave game
        log.info("Disconnect: %s", close_code)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def join(self, msg: dict):
        username = msg["username"]
        if "username" not in self.scope["session"]:
            self.scope["session"]["username"] = username
            self.scope["session"].save()
        self.username = self.scope["session"]["username"]
        log.info("User %s: Joining game", self.username)
        await self.channel_layer.send(
            "game_engine",
            {"type": "player.new", "player": self.username, "channel": self.channel_name},
        )

    async def direction(self, msg: dict):
        if not self.username:
            log.info("Attempting to change direction without joining the game")
            return

        log.info("User %s changing direction", self.username)
        await self.channel_layer.send(
            "game_engine",
            {"type": "player.direction", "player": self.username, "direction": msg["direction"]},
        )

    # Receive message from Websocket
    async def receive(self, text_data=None, bytes_data=None):
        content = json.loads(text_data)
        msg_type = content["type"]
        msg = content["msg"]
        if msg_type == "direction":
            return await self.direction(msg)
        elif msg_type == "join":
            return await self.join(msg)
        else:
            log.warn("Incoming msg %s is unknown", msg_type)

    # Send game data to room group after a Tick is processed
    async def game_update(self, event):
        log.info("Game Update: %s", event)
        # Send message to WebSocket
        state = event["state"]
        await self.send(json.dumps(state))


class GameConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        """
        Created on demand when the first player joins.
        """
        log.info("Game Consumer: %s %s", args, kwargs)
        super().__init__(*args, **kwargs)
        self.group_name = "snek_game"
        self.engine = GameEngine(self.group_name)
        self.engine.start()

    def player_new(self, event):
        log.info("Player Joined: %s", event["player"])
        self.engine.join_queue(event["player"])

    def player_direction(self, event):
        log.info("Player direction changed: %s", event)
        direction = event.get("direction", "UP")

        try:
            direction = Direction[direction]
        except KeyError:
            log.info("Bad Direction! %s", direction)
            return

        self.engine.set_player_direction(event["player"], direction)
