from channels.routing import ProtocolTypeRouter
from channels.routing import route
from core.consumers import ws_connect, ws_disconnect


application = ProtocolTypeRouter({
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
            
            path('whole1/',PracticeConsumer())
            ])
        )
    )
})


channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
]
