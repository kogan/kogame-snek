from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property


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


class Board(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tick = models.PositiveIntegerField(default=0)
    state = JSONField()

    def __str__(self):
        return 'Board<id={0}, tick={1}>: {2}'.format(
            self.pk, self.tick, self.game
        )
