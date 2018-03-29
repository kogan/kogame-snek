import logging
import random
import threading
import time
from collections import OrderedDict
from enum import Enum, unique
from typing import List, Mapping, Optional, Set

import attr
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

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

    def render(self):
        return (self.x, self.y)


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

    def render(self):
        return {
            'username': self.username,
            'snake': [coords.render() for coords in self.snake],
            'alive': self.alive,
            'direction': self.direction.name,
        }

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

    def render(self):
        return {
            'dimensions': self.dimensions.render(),
            'tick': self.tick,
            'food': [f.render() for f in self.food],
            'blocks': [b.render() for b in self.blocks],
        }


@attr.s
class State:
    board: Board = attr.ib(default=attr.Factory(Board), validator=attr.validators.instance_of(Board))
    players: Mapping[str, Player] = attr.ib(default=attr.Factory(dict))

    @staticmethod
    def from_dict(state_dict):
        return State(
            board=Board.from_dict(state_dict['board']),
            players=[Player.from_dict(player) for player in state_dict['players']],
        )

    def render(self):
        return {
            'board': self.board.render(),
            'players': {username: p.render() for username, p in self.players.items()}
        }


class GameEngine(threading.Thread):
    INVALID_MOVES = {
        (Direction.UP, Direction.DOWN),
        (Direction.DOWN, Direction.UP),
        (Direction.LEFT, Direction.RIGHT),
        (Direction.RIGHT, Direction.LEFT),
    }

    dimensions = [30, 30]
    tick_rate = 0.2

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
        self.state = State(board=Board(dimensions=Coords(*self.dimensions)))
        self.direction_changes: Mapping[str, Direction] = {}
        self.direction_lock = threading.Lock()
        self.player_queue = OrderedDict()
        self.player_lock = threading.Lock()

    def run(self):
        log.info('Starting engine loop')
        while True:
            self.state = self.tick()
            self.broadcast_state(self.state)
            time.sleep(self.tick_rate)

    def broadcast_state(self, state: State):
        state_json = state.render()
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'game_update',
                'state': state_json,
            }
        )

    def tick(self) -> State:
        self.game.tick += 1
        log.info('Tick %d for game %s', self.game.tick, self.game)
        state = self.state
        with self.direction_lock:
            movements = self.direction_changes.copy()
            self.direction_changes.clear()
        state = self.process_movements(self.game, state, movements)
        state = self.process_collisions(self.game, state)
        state = self.process_new_players(self.game, state)
        state = self.add_food(self.game, state)
        state.board.tick = self.game.tick
        self.game.save()
        return state

    def set_player_direction(self, player: str, direction: Direction):
        log.info('Setting player direction: %s (%s)', player, direction.name)
        with self.direction_lock:
            self.direction_changes[player] = direction

    def join_queue(self, player: str, at_front=False):
        log.info('Player %s joining queue (Front? %r)', player, at_front)
        with self.player_lock:
            self.player_queue[player] = True
            if at_front:
                self.player_queue.move_to_end(player, last=False)

    def get_queued_player(self) -> Optional[str]:
        log.info('Getting next player in queue')
        with self.player_lock:
            try:
                player, _ = self.player_queue.popitem(last=False)
                return player
            except KeyError:
                # no player queued
                return None

    def process_movements(self, game, state: State, movements) -> State:
        log.info('Processing movements for game: %s', game)
        # Process movement updates for each player
        for player in state.players.values():

            # only update alive players
            if not player.alive:
                continue

            # update player direction if we've got a new one in movements
            if player.username in movements:
                new_direction = movements[player.username]
                # validate movement is a valid choice:
                if new_direction == player.direction:
                    pass
                elif (new_direction, player.direction) in self.INVALID_MOVES:
                    log.info("Invalid movement selected for Player: %s in %s", player.username, game)
                else:
                    player.direction = new_direction

            # update snake with new head and all but last block of current snake
            player.move()

        return state

    def process_collisions(self, game, state: State) -> State:
        log.info('Processing collisions for game: %s', game)
        for player in state.players.values():
            if not player.alive:
                continue

            head = player.snake[0]

            # wall collision
            if (
                head.x < 0 or head.x >= self.dimensions[0] or
                head.y < 0 or head.y >= self.dimensions[1]
            ):
                log.info("Player %s hit a wall in game: %s", player.username, game)
                player.alive = False

            # other player collision
            other_players = [p for p in state.players.values() if p != player and p.alive]
            for other in other_players:
                if head in other.snake:
                    log.info("Player %s hit Player %s in game: %s", player.username, other.username, game)
                    player.alive = False

            # self collision
            if head in player.snake[1:]:
                log.info("Player %s in %s hit self", player.username, game)
                player.alive = False

            # blocks
            # blocks = {(x, y): username for (x, y, username) in board.state['blocks']}
            # if tuple(head) in blocks:
            #    log.info("Player %s hit a block at %s from player %s",
            #              player['username'], head, blocks[head])
            #    player['alive'] = False
            #    collisions.append("%s hit a block" % player['username'])

            # food
            if head in state.board.food:
                # Grow our tail by growth_factor in the same block as our tail
                for x in range(game.growth_factor):
                    player.snake.append(player.snake[-1])

                log.info("Player %s ate food at pos %s in game: %s", player.username, head, game)

                # remove food
                state.board.food.remove(head)

        return state

    def process_new_players(self, game, state: State) -> State:
        log.info('Processing new players for game: %s', game)
        username = self.get_queued_player()
        if not username:
            return state

        player = state.players.pop(username, None)
        if player:
            log.info('Player %s is rejoining. (Alive? %r)', username, player.alive)

        log.info('Trying to add new snake for %s', username)

        # generate random position and add to state
        dims = self.dimensions
        c = Coords(
            x=random.randint(0, dims[0] - 1),
            y=random.randint(0, dims[1] - 1)
        )
        # direct it away from the closest walls, and stretch out that direction 3 squares
        x_mid, y_mid = dims[0] // 2, dims[1] // 2
        x_dir = Direction.LEFT if c.x > x_mid else Direction.RIGHT
        y_dir = Direction.UP if c.y > y_mid else Direction.DOWN
        direction = random.choice((x_dir, y_dir))
        body = c.move(direction)
        head = body.move(direction)
        snake = [head, body, c]

        # check that we don't intersect with any other snek, otherwise put back
        # into queue and wait for next tick (could be costly looping and checking)
        set_snake = set(snake)
        for player in state.players.values():
            if player.alive and set(player.snake) & set_snake:
                log.info('New snake was created on existing snake for %s', username)
                # collision, put player back in queue
                self.join_queue(player, at_front=True)
                return state

        p = Player(username=username, snake=snake, alive=True, direction=direction)
        state.players[username] = p
        log.info('New snake added for %s', username)
        return state

    def add_food(self, game, state: State) -> State:
        log.info('Adding food to game: %s', game)
        # 1 less food than num players, but at least 1 for testing (0 for leaderboards)
        if len(state.board.food) < max(len(state.players) - 1, 1):
            available = set()
            dims = self.dimensions
            for row in range(dims[0]):
                for col in range(dims[1]):
                    available.add(Coords(row, col))

            for player in state.players.values():
                for pos in player.snake:
                    available.discard(pos)

            for food in state.board.food:
                available.remove(food)

            pos = random.choice(list(available))

            state.board.food.add(pos)
        return state
