from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from django.conf.urls import url
from game.consumers import GameConsumer, PlayerConsumer

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "websocket": SessionMiddlewareStack(
        URLRouter([
            url(r'^ws/game/$', PlayerConsumer),
            url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
        ])
    ),
    'channel': ChannelNameRouter({
        'game_engine': GameConsumer,
    }),
})
