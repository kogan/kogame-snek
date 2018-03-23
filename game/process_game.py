import logging

from .models import Board

from .players import Direction

log = logging.getLogger(__name__)


def process_game_state(game):

    # fetch movements from cache
    log.debug("fetching movements for game: %s", game)
    movements = get_movements(game)

    # Update all snakes with their directions
    log.debug("pricessing movements for game: %s", game)
    new_state = process_movements(game, movements)

    # Has anyone hit a wall or another snake?
    log.debug("processing collisions for game: %s", game)
    new_state = process_collisions(game, new_state)

    # Drop new fruit
    log.debug("dropping fruit for game: %s", game)
    new_state = add_fruit(game)

    # Save new game state
    log.debug("saving game state for game: %s", game)
    board = Board.objects.create(state=new_state, game=game)

    # successful update
    return board


def move_block(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])


def process_movements(game, movements):

    state = game.state
    # Process movement updates for each player
    for player in state['players']:

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
