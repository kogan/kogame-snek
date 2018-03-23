from enum import Enum, unique
from typing import List, Mapping

import attr
from django.core.cache import cache
from redis.client import StrictRedis


@unique
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


@attr.s
class Coords:
    x: int = attr.ib(validator=attr.validators.instance_of(int))
    y: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s
class Player:
    username = attr.ib()
    snake: List[Coords] = attr.ib()
    alive: bool = attr.ib(validator=attr.validators.instance_of(bool))
    direction: Direction = attr.ib(validator=attr.validators.in_(Direction))


def set_player_direction(game, player: str, direction: Direction):
    redis: StrictRedis = cache.client.get_client()
    hash_key = f'playerdirections.{game.pk}'
    return redis.hset(hash_key, player, direction.name)


def get_player_directions(game) -> Mapping[str, Direction]:
    redis: StrictRedis = cache.client.get_client()
    hash_key = f'playerdirections.{game.pk}'
    directions: Mapping[bytes, bytes] = redis.hgetall(hash_key)
    return {
        player.decode('utf8'): Direction[direction.decode('utf8')]
        for player, direction in directions.items()
    }
    return directions
