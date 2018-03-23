from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from game.consumers import GameConsumer, PlayerConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/game/$', PlayerConsumer),
        ]),
    ),
    'channel': ChannelNameRouter({
        'game_engine': GameConsumer,
    }),
})
