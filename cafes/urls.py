from django.urls import path


app_name = "cafes"

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
]
