from django.conf import settings
from django.views.generic import ListView

from cafes.models import Cafe


class CafeListView(ListView):
    model = Cafe
    paginate_by = settings.PAGINATE_BY
