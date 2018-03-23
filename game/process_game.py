import logging

log = logging.getLogger(__name__)


def process_game_state(game):

    # fetch movements from cache
    log.debug("fetching movements for game: %s, tick: %s", game.pk, game.tick)
    movements = get_movements(game)

    # Update all snakes with their directions
    log.debug("pricessing movements for game: %s, tick: %s", game.pk, game.tick)
    new_state = process_movements(game, movements)

    # Has anyone hit a wall or another snake?
    log.debug("processing collisions for game: %s, tick: %s", game.pk, game.tick)
    new_state = process_collisions(game, new_state)

    # Drop new fruit
    log.debug("dropping fruit for game: %s, tick: %s", game.pk, game.tick)
    new_state = add_fruit(game)

    # Save new game state
    log.debug("saving game state for game: %s, tick: %s", game.pk, game.tick)
    board = Board.objects.create(state=new_state, game=game)

    # successful update
    return True
