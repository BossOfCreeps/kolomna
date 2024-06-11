from django.contrib import admin

from tickets.models import BasketEvent


@admin.register(BasketEvent)
class BasketEventAdmin(admin.ModelAdmin):
    pass
