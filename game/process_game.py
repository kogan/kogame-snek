import logging

from .players import Direction

log = logging.getLogger(__name__)


def process_game_state(game, movements=None):

    if movements is None:
        # fetch movements from cache
        log.info("fetching movements for game: %s", game)
        movements = get_movements(game)

    # Update all snakes with their directions
    log.info("processing movements for game: %s", game)
    new_state = process_movements(game, movements)

    # Has anyone hit a wall or another snake?
    log.info("processing collisions for game: %s", game)
    new_state, collisions = process_collisions(game, new_state)

    # Drop new fruit
    log.info("dropping fruit for game: %s", game)
    new_state = add_fruit(game, new_state)

    # successful update
    return new_state


def get_movements(game):
    return {}


def move_block(pos, direction):
    return [pos[0] + direction[0], pos[1] + direction[1]]


def compare_in(pos1, pos_list):
    # make sure we're comparing tuples to tuples
    return tuple(pos1) in list(map(tuple, pos_list))


def process_movements(game, movements):

    state = game.current_board.state
    # Process movement updates for each player
    for player in state['players']:

        # only update alive players
        if not player['alive']:
            continue

        # update player direction if we've got a new one in movements
        if player['username'] in movements:
            new_direction = movements[player['username']]

            # validate movement is a valid choice:
            if (new_direction, tuple(player['direction'])) in (
                    (Direction.UP.value, Direction.DOWN.value),
                    (Direction.DOWN.value, Direction.UP.value),
                    (Direction.LEFT.value, Direction.RIGHT.value),
                    (Direction.RIGHT.value, Direction.LEFT.value)
            ):
                log.info("Invalid movement selected for Player: %s in %s", player['username'], game)
            else:
                player['direction'] = new_direction

        snake = player['snake']

        # update snake with new head and all but last block of current snake
        head = move_block(player['snake'][0], player['direction'])
        player['snake'] = [head] + snake[:-1]

    return state


def process_collisions(game, state):

    board = game.current_board

    collisions = []
    for player in state['players']:

        head = player['snake'][0]

        # wall collision
        if (
            head[0] < 0 or head[0] >= board.dimensions[0] or
            head[1] < 0 or head[1] >= board.dimensions[1]
        ):
            log.info("Player %s in %s hit a wall", player['username'], game)
            player['alive'] = False
            collisions.append("%s hit a wall" % player['username'])

        # other player collision
        other_players = [p for p in state['players'] if p != player and p['alive']]
        for other in other_players:
            if compare_in(head, other['snake']):
            #if head in other['snake']:
                log.info("Player %s in %s hit Player: %s", player['username'], game, other['username'])
                player['alive'] = False
                collisions.append("%s hit %s" % (player['username'], other['username']))

        # self collision
        if compare_in(head, player['snake'][1:]):
        #if head in player['snake'][1:]:
            log.info("Player %s in %s hit self", player['username'], game)
            player['alive'] = False
            collisions.append("%s hit self" % player['username'])

        # blocks
        #blocks = {(x, y): username for (x, y, username) in board.state['blocks']}
        #if tuple(head) in blocks:
        #    log.info("Player %s hit a block at %s from player %s",
        #              player['username'], head, blocks[head])
        #    player['alive'] = False
        #    collisions.append("%s hit a block" % player['username'])

        # food
        if compare_in(head, board.state['food']):
        #if head in board.state['food']:
            # Grow our tail by growth_factor in the same block as our tail
            for x in range(game.growth_factor):
                player['snake'].append(player['snake'][-1])

            log.info("Player %s ate food at pos %s in %s", player['username'], head, game)
            collisions.append("%s hit a food block" % player['username'])

            # remove food
            board['food'].remove(head)

    return state, collisions


def add_fruit(game, state):
    return state
