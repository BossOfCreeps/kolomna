from django.urls import path

from tickets.views import (
    BasketView,
    BuyBasketView,
    EventBuyView,
    EventDeleteView,
    PurchaseDetailView,
    PurchaseApproveView,
)

app_name = "tickets"

urlpatterns = [
    path("basket", BasketView.as_view(), name="basket"),
    path("basket/buy", BuyBasketView.as_view(), name="basket-buy"),
    path("events/<int:pk>/delete", EventDeleteView.as_view(), name="event-delete"),
    path("events/buy", EventBuyView.as_view(), name="event-buy"),
    path("purchase/<int:pk>", PurchaseDetailView.as_view(), name="purchase-detail"),
    path("purchase/approve", PurchaseApproveView.as_view(), name="purchase-approve"),
]
