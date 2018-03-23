import logging

from .players import Direction

log = logging.getLogger(__name__)


def process_game_state(game, movements=None):

    if movements is None: 
        # fetch movements from cache
        log.debug("fetching movements for game: %s", game)
        movements = get_movements(game)

    # Update all snakes with their directions
    log.debug("pricessing movements for game: %s", game)
    new_state = process_movements(game, movements)

    # Has anyone hit a wall or another snake?
    log.debug("processing collisions for game: %s", game)
    new_state, collisions = process_collisions(game, new_state)

    # Drop new fruit
    log.debug("dropping fruit for game: %s", game)
    new_state = add_fruit(game, new_state)

    # successful update
    return new_state


def get_movements(game):
    return {}


def move_block(pos, direction):
    return [pos[0] + direction[0], pos[1] + direction[1]]


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
            if (new_direction, player['direction']) in (
                    (Direction.UP, Direction.DOWN),
                    (Direction.DOWN, Direction.UP),
                    (Direction.LEFT, Direction.RIGHT),
                    (Direction.RIGHT, Direction.LEFT)
            ):
                log.debug("Invalid movement selected for Player: %s in %s",
                          player['username'], game)

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

        head = list(player['snake'][0])

        # wall collision
        if head[0] < 0 or head[0] >= board.dimensions[0] or \
                head[1] < 0 or head[1] >= board.dimensions[1]:
            log.debug("Player %s in %s hit a wall", player['username'], game)
            player['alive'] = False
            collisions.append("%s hit a wall" % player['username'])

        # other player collision
        other_players = [p for p in state['players'] if p != player and p['alive']]
        for other in other_players:
            if head in other['snake']:
                log.debug("Player %s in %s hit Player: %s",
                          player['username'], game, other['username'])
                player['alive'] = False
                collisions.append("%s hit %s" % (player['username'], other['username']))

        # self collision
        if head in player['snake'][1:]:
            log.debug("Player %s in %s hit self",
                      player['username'], game)
            player['alive'] = False
            collisions.append("%s hit self" % player['username'])

        # blocks
        #blocks = {(x, y): username for (x, y, username) in board.state['blocks']}
        #if tuple(head) in blocks:
        #    log.debug("Player %s hit a block at %s from player %s",
        #              player['username'], head, blocks[head])
        #    player['alive'] = False
        #    collisions.append("%s hit a block" % player['username'])

        # food
        if head in board.state['food']:
            # Grow our tail by growth_factor in the same block as our tail
            for x in range(game.growth_factor):
                player['snake'].append(player['snake'][-1])

            log.debug("Player %s ate food at pos %s in %s",
                      player['username'], head, game)
            collisions.append("%s hit a food block" % player['username'])

            # remove food
            board['food'].remove(head)

    return state, collisions


def add_fruit(game, state):
    return state
