from django.contrib.auth import login
from django.views.generic import FormView

from users.forms import RegistrationForm
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
