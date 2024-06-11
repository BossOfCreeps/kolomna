from django.urls import path

from tickets.views import BasketView, BuyBasketView, EventBuyView

app_name = "tickets"

urlpatterns = [
    path('basket', BasketView.as_view(), name='basket'),
    path('basket/buy', BuyBasketView.as_view(), name='basket-buy'),
    path("events/buy", EventBuyView.as_view(), name="event-buy"),
]
