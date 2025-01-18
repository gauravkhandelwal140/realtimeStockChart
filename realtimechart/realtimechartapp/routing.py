from django.urls import path

from .consumers import StockConsumer

ws_urlpatterns = [
    path('ws/stockcharts/', StockConsumer.as_asgi()),
]