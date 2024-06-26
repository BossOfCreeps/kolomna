from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin", admin.site.urls),
    path("", include("core.urls")),
    path("events/", include("events.urls")),
    path("tickets/", include("tickets.urls")),
    path("users/", include("users.urls")),
    path("cafes/", include("cafes.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
