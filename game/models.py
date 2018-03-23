from django.contrib.postgres.fields import JSONField
from django.db import models


class Game(models.Model):
    started = models.DateTimeField(auto_now_add=True)
    tick = models.PositiveIntegerField()

    def __str__(self):
        return 'Game<pk={0}, tick={1}, started={2}>'.format(
            self.pk, self.tick, self.started
        )

    @property
    def current_board(self):
        return self.board_list.order_by('-tick').first()


class Board(models.Model):

    dimensions = [50,50]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tick = models.PositiveIntegerField()
    state = JSONField()

    def __str__(self):
        return 'Board<id={0}, tick={1}>: {2}'.format(
            self.pk, self.tick, self.game
        )
