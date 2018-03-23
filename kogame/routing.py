from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from game.consumers import GameConsumer

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url(r'^game/$', GameConsumer),
        url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    ]),
})
