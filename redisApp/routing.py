from django.urls import path
from . import consumers
websocket_urlpatterns=[
    path('ws/async',consumers.MyAsyncConsumer.as_asgi()),
    path('ws/async/<str:slug>',consumers.MyAsyncConsumer.as_asgi())
]