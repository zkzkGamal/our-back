from django.urls import re_path
from . import consumer

websocket_patterns = [
    re_path(r'ws/notify/' , consumer.Notification.as_asgi()),
    re_path(r'ws/chat/' , consumer.Chat_doctor.as_asgi())

]