from django.urls import path

from users.views import RegistrationView, LoginView, ProfileView

app_name = "users"

urlpatterns = [
    path("reg", RegistrationView.as_view(), name="registration"),
    path("login", LoginView.as_view(), name="login"),
    path("", ProfileView.as_view(), name="profile"),
]
