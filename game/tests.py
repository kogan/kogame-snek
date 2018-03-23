from django.test import TestCase

from .models import Board, Game
from .players import Direction, get_player_directions, set_player_direction


class PlayerTests(TestCase):

    def test_basic(self):
        self.assertTrue(True)

    def test_get_player_directions(self):
        game = Game.objects.create(tick=0)
        pname = 'josh'
        set_player_direction(game, pname, Direction.UP)
        directions = get_player_directions(game)
        self.assertEqual(directions, {
            'josh': Direction.UP,
        })
