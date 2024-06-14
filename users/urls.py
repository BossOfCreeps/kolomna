from django.urls import path

from users.views import RegistrationView, LoginView, ProfileView, LogoutView, ProfileHistoryView, ProfileSavedView

app_name = "users"

urlpatterns = [
    path("reg", RegistrationView.as_view(), name="registration"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("", ProfileView.as_view(), name="profile"),
    path("history", ProfileHistoryView.as_view(), name="profile-history"),
    path("saved", ProfileSavedView.as_view(), name="profile-saved"),
]
