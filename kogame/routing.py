from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from django.conf.urls import url
from game.consumers import GameConsumer, PlayerConsumer

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "websocket": SessionMiddlewareStack(
    'websocket': URLRouter([
        url(r'^ws/game/$', GameConsumer),
        url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    ]),
    ),
    'channel': ChannelNameRouter({
        'game_engine': GameConsumer,
    }),
})
