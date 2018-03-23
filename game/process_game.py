import logging
import random

from .engine import (
    Coords, Direction, Player, State, get_player_directions, get_queued_player,
    join_queue,
)

log = logging.getLogger(__name__)


def process_game_state(game, movements=None):

    if movements is None:
        # fetch movements from cache
        log.info("fetching movements for game: %s", game)
        movements = get_player_directions(game)

    # Update all snakes with their directions
    log.info("processing movements for game: %s", game)
    new_state = process_movements(game, movements)

    # Has anyone hit a wall or another snake?
    log.info("processing collisions for game: %s", game)
    new_state, collisions = process_collisions(game, new_state)

    # Player has joined the game
    log.info("processing new players for game %s", game)
    new_state = process_new_players(game, new_state)

    # Drop new fruit
    log.info("dropping fruit for game: %s", game)
    new_state = add_food(game, new_state)

    # successful update
    return new_state


def process_movements(game, movements) -> State:

    state: State = game.current_board.loaded_state
    # Process movement updates for each player
    for player in state.players:

        # only update alive players
        if not player.alive:
            continue

        # update player direction if we've got a new one in movements
        if player.username in movements:
            new_direction = movements[player.username]

            # validate movement is a valid choice:
            if (new_direction, tuple(player.direction)) in (
                    (Direction.UP.value, Direction.DOWN.value),
                    (Direction.DOWN.value, Direction.UP.value),
                    (Direction.LEFT.value, Direction.RIGHT.value),
                    (Direction.RIGHT.value, Direction.LEFT.value)
            ):
                log.info("Invalid movement selected for Player: %s in %s", player.username, game)
            else:
                player.direction = new_direction

        # update snake with new head and all but last block of current snake
        player.move()

    return state


def process_collisions(game, state: State):

    board = game.current_board

    collisions = []
    for player in state.players:

        head = player.snake[0]

        # wall collision
        if (
            head.x < 0 or head.x >= board.dimensions[0] or
            head.y < 0 or head.y >= board.dimensions[1]
        ):
            log.info("Player %s in %s hit a wall", player.username, game)
            player.alive = False
            collisions.append("%s hit a wall" % player.username)

        # other player collision
        other_players = [p for p in state.players if p != player and p.alive]
        for other in other_players:
            if head in other.snake:
                log.info("Player %s in %s hit Player: %s", player.username, game, other.username)
                player.alive = False
                collisions.append("%s hit %s" % (player.username, other.username))

        # self collision
        if head in player.snake[1:]:
            log.info("Player %s in %s hit self", player.username, game)
            player.alive = False
            collisions.append("%s hit self" % player.username)

        # blocks
        #blocks = {(x, y): username for (x, y, username) in board.state['blocks']}
        #if tuple(head) in blocks:
        #    log.info("Player %s hit a block at %s from player %s",
        #              player['username'], head, blocks[head])
        #    player['alive'] = False
        #    collisions.append("%s hit a block" % player['username'])

        # food
        if head in state.food:
            # Grow our tail by growth_factor in the same block as our tail
            for x in range(game.growth_factor):
                player.snake.append(player.snake[-1])

            log.info("Player %s ate food at pos %s in %s", player.username, head, game)
            collisions.append("%s hit a food block" % player.username)

            # remove food
            state.food.remove(head)

    return state, collisions


def add_food(game, state):
    # 1 less food than num players, but at least 1 for testing (0 for leaderboards)
    if len(state.food) < max(len(state.players) - 1, 1):
        available = set()
        dims = game.current_board
        for row in range(dims[0]):
            for col in range(dims[1]):
                available.add(Coords(row, col))

        for player in state.players:
            for pos in player.snake:
                try:
                    available.remove(pos)
                except KeyError:
                    continue

        for food in state.food:
            available.remove(food)

        pos = random.choice(list(available))

        state.food.append(pos)
    return state


def process_new_players(game, state):
    player = get_queued_player(game)
    if not player:
        return state

    board = game.current_board

    # generate random position and add to state
    dims = board.dimensions
    c = Coords(
        x=random.randint(0, dims[0]),
        y=random.randint(0, dims[1])
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
    for player in state.players:
        if set(player.snake) & set_snake:
            # collision, put player back in queue
            join_queue(game, player, at_front=True)
            return state

    p = Player(username=player, snake=snake, alive=True, direction=direction)
    state.players.append(p)
    return state
