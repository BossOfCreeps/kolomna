from django.urls import path

from tickets.views import BasketView, BuyBasketView

app_name = "tickets"

urlpatterns = [
    path('', BasketView.as_view(), name='basket'),
    path('buy/', BuyBasketView.as_view(), name='basket-buy'),
]
