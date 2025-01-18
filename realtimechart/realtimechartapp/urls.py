from django.urls import path

from .views import index,get_initial_data

urlpatterns = [
    path('', index),
    path('api/stocks/initial/', get_initial_data, name='get_initial_data'),
]