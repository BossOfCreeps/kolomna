from django.urls import path

from tickets.views import (
    BasketView,
    BuyBasketView,
    EventBuyView,
    EventDeleteView,
    PurchaseDetailView,
    PurchaseApproveView,
    PurchaseReviewView,
    PurchaseDeleteView,
)

app_name = "tickets"

urlpatterns = [
    path("basket", BasketView.as_view(), name="basket"),
    path("basket/buy", BuyBasketView.as_view(), name="basket-buy"),
    path("events/<int:pk>/delete", EventDeleteView.as_view(), name="event-delete"),
    path("events/buy", EventBuyView.as_view(), name="event-buy"),
    path("purchase/<int:pk>", PurchaseDetailView.as_view(), name="purchase-detail"),
    path("purchase/<int:pk>/delete", PurchaseDeleteView.as_view(), name="purchase-delete"),
    path("purchase/approve", PurchaseApproveView.as_view(), name="purchase-approve"),
    path("purchase/review", PurchaseReviewView.as_view(), name="purchase-review"),
]
