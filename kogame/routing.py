from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from django.conf.urls import url
from game.consumers import GameConsumer, PlayerConsumer

application = ProtocolTypeRouter({
    "websocket": SessionMiddlewareStack(
        URLRouter([
            url(r'^ws/game/$', PlayerConsumer),
        ]),
    ),
    'channel': ChannelNameRouter({
        'game_engine': GameConsumer,
    }),
})
