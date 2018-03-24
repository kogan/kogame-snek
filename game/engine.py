import logging
import threading
import time
from enum import Enum, unique
from typing import List, Mapping, Set

import attr
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from redis.client import StrictRedis

log = logging.getLogger(__name__)


@unique
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


@attr.s(frozen=True)
class Coords:
    x: int = attr.ib(validator=attr.validators.instance_of(int))
    y: int = attr.ib(validator=attr.validators.instance_of(int))

    def move(self, direction: Direction) -> 'Coords':
        dx, dy = direction.value
        return Coords(self.x + dx, self.y + dy)


@attr.s
class Player:
    username = attr.ib()
    snake: List[Coords] = attr.ib()
    alive: bool = attr.ib(validator=attr.validators.instance_of(bool))
    direction: Direction = attr.ib(validator=attr.validators.in_(Direction))

    @staticmethod
    def from_dict(state_dict):
        return Player(
            username=state_dict['username'],
            snake=[Coords(**part) for part in state_dict['snake']],
            alive=state_dict['alive'],
            direction=Direction[state_dict['direction']],
        )

    def move(self):
        """
        Updates the snake, moving the head in direction, and chopping the last
        block.
        """
        new_head = self.snake[0].move(self.direction)
        self.snake = [new_head] + self.snake[:-1]


@attr.s
class Board:
    dimensions: Coords = attr.ib(default=Coords(50, 50))
    tick: int = attr.ib(default=0, validator=attr.validators.instance_of(int))
    food: Set[Coords] = attr.ib(default=attr.Factory(set))
    blocks: Set[Coords] = attr.ib(default=attr.Factory(set))

    @staticmethod
    def from_dict(state_dict):
        return Board(
            dimensions=Coords(**state_dict['dimensions']),
            tick=state_dict['tick'],
            food={Coords(**food) for food in state_dict['food']},
            blocks={Coords(**block) for block in state_dict['blocks']},
        )


@attr.s
class State:
    board: Board = attr.ib(default=attr.Factory(Board), validator=attr.validators.instance_of(Board))
    players: List[Player] = attr.ib(default=attr.Factory(list))

    @staticmethod
    def from_dict(state_dict):
        return State(
            board=Board.from_dict(state_dict['board']),
            players=[Player.from_dict(player) for player in state_dict['players']],
        )

    def for_json(self):
        """
        Converts state into a dictionary that can be encoded and decoded by
        JSON. Nececessary because Enums aren't encoded correctly.
        """
        dict_state = attr.asdict(self)
        for player in dict_state['players']:
            player['direction'] = player['direction'].name
        return dict_state


def set_player_direction(game, username: str, direction: Direction):
    redis: StrictRedis = cache.client.get_client()
    hash_key = f'playerdirections.{game.pk}'
    return redis.hset(hash_key, username, direction.name)


def get_player_directions(game) -> Mapping[str, Direction]:
    redis: StrictRedis = cache.client.get_client()
    hash_key = f'playerdirections.{game.pk}'
    directions: Mapping[bytes, bytes] = redis.hgetall(hash_key)
    return {
        player.decode('utf8'): Direction[direction.decode('utf8')]
        for player, direction in directions.items()
    }
    return directions


def join_queue(game, username: str, at_front=False):
    redis: StrictRedis = cache.client.get_client()
    hash_key = f'playerqueue.{game.pk}'
    if at_front:
        return redis.lpush(hash_key, username)
    return redis.rpush(hash_key, username)


def get_queued_player(game):
    # only one player can join at a time
    redis: StrictRedis = cache.client.get_client()
    hash_key = f'playerqueue.{game.pk}'
    username = redis.lpop(hash_key)
    return username if username is None else username.decode('utf8')


class GameEngine(threading.Thread):
    def __init__(self, game, group_name, **kwargs):
        log.info('Init GameEngine...')
        super(GameEngine, self).__init__(
            daemon=True,
            name='GameEngine',
            **kwargs
        )
        self.group_name = group_name
        self.channel_layer = get_channel_layer()
        self.game = game

    def run(self):
        log.info('Starting engine loop')
        while True:
            state = self.game.game_tick()
            self.broadcast_state(state)
            time.sleep(0.5)

    def broadcast_state(self, state):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'game_update',
                'state': state,
            }
        )
