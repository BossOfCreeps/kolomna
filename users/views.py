from django.contrib.auth import login
from django.views.generic import FormView, TemplateView

from users.forms import RegistrationForm, LoginForm
from users.models import CustomUser


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = "users/reg.html"
    success_url = "/"

    def form_valid(self, form):
        user = CustomUser.objects.create_user(
            form.cleaned_data["email"],
            form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
        )
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    form_class = LoginForm

    def get_success_url(self):
        return self.request.GET.get("next", "/")

    def form_valid(self, form):
        user = CustomUser.objects.get(email=form.cleaned_data["email"])
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(TemplateView):
    template_name = "users/profile.html"
