import logging
import sys
from time import sleep, time

from django.core.management.base import BaseCommand
from game.models import Game

log = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        tick_duration = 5  # seconds

        # create Game instance with board
        game = Game.objects.create(tick_duration=tick_duration)

        game.init_board()

        # run loop
        while True:
            now = time.time()
            result = game.process_game_state()
            if result is False:
                break

            next_tick = now + tick_duration
            self.sleep_till(next_tick)

        log.info("Game finished. Ran for %s ticks", game.ticks)

    def sleep_till(when):

        nap_time = when - time.time()

        if nap_time < 0:
            log.exception("Missed tick. Aborting!")
            sys.exit(1)

        sleep(nap_time)
