from django.contrib.auth import login, logout
from django.db.models import Max, Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import FormView, TemplateView, View

from tickets.models import Purchase, PurchaseStatus
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = Purchase.objects.annotate(start_at=Max("events__start_at")).filter(
            user=self.request.user,
            status__in=[PurchaseStatus.SUCCESS.value, PurchaseStatus.NEW.value],
            start_at__gte=timezone.now(),
        )
        return context


class ProfileHistoryView(TemplateView):
    template_name = "users/profile-history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = (
            Purchase.objects.annotate(start_at=Max("events__start_at"))
            .filter(user=self.request.user)
            .filter(Q(status=PurchaseStatus.CLOSED.value) | Q(start_at__lte=timezone.now()))
        )
        return context


class ProfileSavedView(TemplateView):
    template_name = "users/profile-saved.html"


class LogoutView(View):
    def get(self, request):
        logout(self.request)
        return redirect(reverse("core:index"))
