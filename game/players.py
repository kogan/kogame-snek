from enum import Enum, unique
from typing import Mapping

from django.core.cache import cache
from redis.client import StrictRedis


@unique
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


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
