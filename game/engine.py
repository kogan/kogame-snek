import logging
import threading
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

log = logging.getLogger(__name__)


class GameEngine(threading.Thread):
    def __init__(self, game, group_name, **kwargs):
        log.info('Init GameEngine...')
        super(GameEngine, self).__init__(
            daemon=True,
            name='GameEngine',
            **kwargs
        )
        self.group_name = group_name
        self.channel_layer = get_channel_layer()
        self.game = kwargs['game']

    def run(self):
        log.info('Starting engine loop')
        while True:
            state = self.game.tick()
            self.broadcast_state(state)
            time.sleep(1)

    def broadcast_state(self, state):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'game_update',
                'state': state,
            }
        )
