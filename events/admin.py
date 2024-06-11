from django.contrib import admin

from events.models import Event, EventImage, Organization, EventSchedule, EventPrice


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    class EventImageInline(admin.TabularInline):
        model = EventImage

    class EventScheduleInline(admin.TabularInline):
        model = EventSchedule

    class EventPriceInline(admin.TabularInline):
        model = EventPrice

    inlines = [EventImageInline, EventScheduleInline, EventPriceInline]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass
