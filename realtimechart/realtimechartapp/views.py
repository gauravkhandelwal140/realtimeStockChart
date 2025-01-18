from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from .models import Stock
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.


def index(request):

    return render(request, 'demo.html', context={'text': 'Hello World!!!'})

# def chart(request):
#
#     return render(request, 'demo.html', context={'text': 'Hello World!!!'})


def get_initial_data(request):
    stocks = Stock.objects.order_by('-dateTime')  # Fetch the last 50 records
    data = [
        {
            "Symbol": stock.symbol,
            "Datetime": stock.dateTime,
            "Open": stock.open,
            "High": stock.high,
            "Low": stock.low,
            "Close": stock.close,
            "Volume": stock.volume,
        }
        for stock in stocks
    ]
    return JsonResponse({"data": data})



def send_stock_update_to_single():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        f"user",  # Group name
        {
            'type': 'send_notification',
            'message': 'message'
        }
    )