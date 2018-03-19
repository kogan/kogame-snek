from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from game.consumers import TestConsumer

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url(r'^test/$', TestConsumer),
        url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    ]),
})
