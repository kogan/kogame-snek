import logging
import sys
from time import sleep, time

import os
import random

from django.core.management.base import BaseCommand
from game.models import Game, Board
from game.players import Direction
from game.process_game import process_game_state

log = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  
log.addHandler(console_handler)        
log.setLevel(logging.DEBUG)    


class Command(BaseCommand):

    def handle(self, *args, **options):

        # create Game instance with board
        game = Game.objects.create(tick=0)
        board = Board.objects.create(game=game, tick=0)

        print(game)
        print("Alive players = {}".format(game.current_board.player_count()))

        board.state['food'] = [(10,10), (40,10)]

        board.state['players'] = [
            {
                'username': 'null@null.kgn.io',
                'snake': [(5,5), (5,6), (5,7), (6,7), (7,7), (8,7), (8,8), (8,9)],
                'direction': (-1,0),
                'alive': True,
                'start_tick': 0,
            },
            {
                'username': 'null2@null.kgn.io',
                'snake': [(10,35), (10,36), (10,37), (10, 38), (10,39)],
                'direction': (-1,0),
                'alive': True,
                'start_tick': 0,
            },
        ]

        board.save()
        
        moves = [
            Direction.LEFT.value,
            Direction.LEFT.value,
            Direction.LEFT.value,
            Direction.LEFT.value,
            Direction.DOWN.value,
            Direction.RIGHT.value,
            Direction.UP.value,
        ]

        for x in range(20):
            
            board = game.current_board

            movements = {}
            for player in board.state['players']:
                movements[player['username']] = random.choice([
                    Direction.UP.value,
                    Direction.DOWN.value,
                    Direction.LEFT.value,
                    Direction.RIGHT.value,
                ])
                #movements[player['username']] = moves[x]


            new_state = process_game_state(game, movements=movements)

            new_board = Board.objects.create(game=game, tick = board.tick+1, state=new_state)

            print_board(game)
            print(game.current_board.state)

            print("Alive players = {}".format(new_board.player_count()))

            if new_board.player_count() == 0:
                print("No players alive")
                break

            input()



def print_board(game):

    board = game.current_board

    state = board.state

    out = []
    for row in range(board.dimensions[1]):
        out.append([' '] * board.dimensions[0])

    # add food
    for food in state['food']:
        out[food[1]][food[0]] = 'F'

    # add snakes
    for i, player in enumerate(state['players']):

        head = player['snake'][0]

        out[head[1]][head[0]] = 'H'

        for pos in player['snake'][1:]:
            out[pos[1]][pos[0]] = '%d' % i

    # print out board
    os.system('clear')
    print('-' * (2+board.dimensions[1]))
    for row in out:
        row_str = '|%s|' % ''.join(row)
        print(row_str)
    print('-' * (2+board.dimensions[1]))
    print("tick: {}".format(board.tick))

    print("Dead players:")
    for player in state['players']:
        if not player['alive']:
            print(" - {}".format(player['username']))
