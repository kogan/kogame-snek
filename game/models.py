import attr
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from .engine import State
from .process_game import process_game_state


class Game(models.Model):

    growth_factor = 2  # How much to grow if we eat food

    started = models.DateTimeField(auto_now_add=True)
    tick = models.PositiveIntegerField(db_index=True)

    def __str__(self):
        return 'Game<pk={0}, tick={1}, started={2}>'.format(
            self.pk, self.tick, self.started
        )

    @cached_property
    def current_board(self) -> 'Board':
        return self.board_set.order_by('-tick').first()

    def game_tick(self):
        self.tick += 1
        new_state = process_game_state(self)
        new_state.tick = self.tick
        dict_state = attr.asdict(new_state)
        # enums aren't serializable :/
        for player in dict_state['players']:
            player['direction'] = player['direction'].name
        board = Board.objects.create(state=dict_state, game=self, tick=self.tick)
        self.save()
        return board.state


class Board(models.Model):

    dimensions = [50, 50]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tick = models.PositiveIntegerField(default=0)
    state = JSONField()

    def save(self, *args, **kwargs):
        if not self.pk and not self.state:
            self.state = {
                "players": [],
                "food": [],
                "blocks": [],
                "tick": 0,
            }
        super(Board, self).save(*args, **kwargs)

    def __str__(self):
        return 'Board<id={0}, tick={1}>: {2}'.format(
            self.pk, self.tick, self.game
        )

    @cached_property
    def loaded_state(self) -> State:
        return State.from_dict(self.state)

    def player_count(self):
        state = self.loaded_state
        return sum(p.alive for p in state.players)
