from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter

from game.consumers import TestConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        url(r"^test/$", TestConsumer),
    ]),
})
