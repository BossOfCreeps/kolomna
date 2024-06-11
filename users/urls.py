from django.urls import path

from users.views import RegistrationView

app_name = "users"

urlpatterns = [
    path('reg', RegistrationView.as_view(), name='registration'),
]
