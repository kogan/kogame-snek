from django.contrib.postgres.fields import JSONField
from django.db import models

from .process_game import process_game_state


class Game(models.Model):

    growth_factor = 2  # How much to grow if we eat food

    started = models.DateTimeField(auto_now_add=True)
    tick = models.PositiveIntegerField(db_index=True)

    def __str__(self):
        return 'Game<pk={0}, tick={1}, started={2}>'.format(
            self.pk, self.tick, self.started
        )

    @property
    def current_board(self):
        return self.board_set.order_by('-tick').first()

    def tick(self):
        new_state = process_game_state(self)
        board = Board.objects.create(state=new_state, game=self)
        self.tick += 1
        self.save()
        return board.state


class Board(models.Model):

    dimensions = [50, 50]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tick = models.PositiveIntegerField()
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

    def player_count(self):
        alive = 0
        for player in self.state['players']:
            if player['alive']:
                alive += 1
        return alive
