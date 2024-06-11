from django.views.generic import ListView

from cafes.models import Cafe


class CafeListView(ListView):
    model = Cafe
