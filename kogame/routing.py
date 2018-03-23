from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from game.consumers import GameConsumer, PlayerConsumer

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url(r'^game/$', PlayerConsumer),
        url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    ]),
    'channel': ChannelNameRouter({
        'game_engine': GameConsumer,
    }),
})
