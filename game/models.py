from django.contrib.postgres.fields import JSONField
from django.db import models


class Board(models.Model):
    state = JSONField()
    tick = models.PositiveIntegerField()
    started = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Board<id={0}, tick={1}>'.format(self.pk, self.tick)


class Game(models.Model):
    board = models.ForeignKey(Board, on_delete=models.PROTECT)

    def __str__(self):
        return 'Game<pk={0}>: {1}'.format(self.pk, self.board)
