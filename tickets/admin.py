from django.contrib import admin

from tickets.models import BasketEvent, Purchase, PurchaseEvent


@admin.register(BasketEvent)
class BasketEventAdmin(admin.ModelAdmin):
    pass


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    class PurchaseEventInline(admin.TabularInline):
        model = PurchaseEvent

    inlines = [PurchaseEventInline]
