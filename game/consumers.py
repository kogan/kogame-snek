import logging

from channels.consumer import SyncConsumer

log = logging.getLogger(__name__)


class TestConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({'type': 'websocket.accept'})

    def websocket_disconnect(self, event):
        pass

    def websocket_receive(self, event):
        pass
