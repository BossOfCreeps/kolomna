from django.urls import path

from cafes.views import CafeListView

app_name = "cafes"

urlpatterns = [
    path("", CafeListView.as_view(), name="cafe-list"),
]
